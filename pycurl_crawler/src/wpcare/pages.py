from crawlerlib.crawler import Crawler

from bs4 import BeautifulSoup

import uuid
import json
import os
from datetime import datetime

ROOT_DIR = os.path.abspath(os.curdir)
DATA_DIR = os.path.join(ROOT_DIR, "data")

PAGES_FILENAME = os.path.join(DATA_DIR, "pages.json")


def get_site_from_url(url):
  url_parts=url.split('/')

  if url.startswith('http'):
    return url_parts[2]
  else:
    return url_parts[0]



def normalize_slash_url(url):
  # TODO: Add domain and https:
  # TODO: Identify files (like .js, .css, name.html, .pdf or images)

  if not url.endswith('/'):
    return url+'/'

  return url



def normalize_link(url, page_url):
  (protocol, void, domain, *path_parts) = page_url.split('/')
  normalized_url = url

  if normalized_url.startswith('//'):
    normalized_url = protocol+normalized_url

  if normalized_url.startswith('/'):
    normalized_url = protocol+'//'+domain+normalized_url

  if normalized_url.startswith('#'):
    normalized_url = page_url+normalized_url

  return normalized_url



def get_link_info_from_bs4(link):
  selector_path = [link.name+('#'+link['id'] if 'id' in link else '')+(''.join('.'+c for c in link.get_attribute_list('class')) if len(link.get_attribute_list('class')) > 0 and link.get_attribute_list('class')[0] is not None else '')]

  for parent in link.parents:
    selector_path.insert(0, parent.name+("#"+parent['id'] if 'id' in parent else '')+(''.join('.'+c for c in parent.get_attribute_list('class')) if len(parent.get_attribute_list('class')) > 0 and parent.get_attribute_list('class')[0] is not None else ''))

    if parent.name == 'body':
      break

  return {
    "href": link.get('href'),
    "html": str(link),
    "css_selector": selector_path
    }



class Page:
  def __init__(self, url_or_id, domain=None):
    if isinstance(url_or_id, str) or isinstance(url_or_id, int):
      if isinstance(url_or_id, int) or url_or_id.isdecimal():
        self.id = int(url_or_id)
        self.url = None
      else:
        self.id = None
        self.url = normalize_slash_url(url_or_id)
 
      self.created_at = None
      self.uuid = None
      self.site = ''
      self.types = []
      self.visited_at = None
      self.links = {
        "navigation": {
          "internal_pages": [],
          "internal_resources": [],
          "external": [],
          "other": []
        },
        "styles": [],
        "scripts": [],
        "images": []
      }

      self.load()

    elif isinstance(url_or_id, dict):
      self.objetivize(url_or_id)

    else:
      raise BaseException("TODO: Not implemented!")

  def addType(self, pageType):
    if pageType not in self.types:
      self.types.append(pageType)

  def removeType(self, pageType):
    if pageType in self.types:
      self.types.remove(pageType)

  def hasType(self, pageType):
    return pageType in self.types

  def getLinks(self):
    now = int(datetime.utcnow().timestamp())

    if self.visited_at is not None and now - self.visited_at < 60:
      print('Recent')
      return

    try:
      crawler = Crawler(self.url)
      crawler.perform()
      html = crawler.get_html()
      self.visited_at = now

    except Exception as e:
      print('ERROR getting ' + url)
      print(e)
      return []

    soup = BeautifulSoup(html, 'html.parser')

    # Links

    all_links = [get_link_info_from_bs4(link) for link in soup.find_all('a') if link.get('href') is not None and link.get('href') != '' ]

    links = {
      "internal_pages": [],
      "internal_resources": [],
      "external": [],
      "other": []
    }

    # TODO: Links starts with //

    for link in all_links:
      normalized_link = normalize_link(link['href'], self.url)
      link['normalized_href'] = normalized_link

      if normalized_link.startswith('/'):
        links['internal_pages'].append(link)
      elif normalized_link.startswith('#'):
        links['internal_pages'].append(link)
      elif normalized_link.startswith(self.site) or normalized_link.startswith('http://'+self.site) or normalized_link.startswith('https://'+self.site):
        links['internal_pages'].append(link)
      elif normalized_link.startswith('http:') or normalized_link.startswith('https:'):
        links['external'].append(link)
      else:
        links['other'].append(link)

    self.links = {
        "navigation": links,
        "styles":  [link.get('src') for link in soup.find_all('link') if link.get('src') is not None and link.get('src') != '' ],
        "scripts":  [link.get('src') for link in soup.find_all('script') if link.get('src') is not None and link.get('src') != '' ],
        "images":  [link.get('src') for link in soup.find_all('img') if link.get('src') is not None and link.get('src') != '' ]
    }

  def initialize(self):
    now = int(datetime.utcnow().timestamp())

    self.created_at = now
    self.uuid = str(uuid.uuid4())
    self.site = get_site_from_url(self.url)

  def serialize(self):
    return {
      "id": self.id,
      "created_at": self.created_at,
      "uuid": self.uuid,
      "url": normalize_slash_url(self.url),
      "site": self.site,
      "types": self.types,
      "visited_at": self.visited_at,
      "links": self.links
    }

  def objetivize(self, data):
    self.id = data['id']
    self.created_at = data["created_at"]
    self.uuid = data['uuid']
    self.url = data['url']
    self.site = data['site']
    self.types = data['types']
    self.visited_at = data['visited_at'] if 'visited_at' in data else None
    self.links = data['links']

  def save(self):
    Pages.create(self)

  def load(self):
    page_data = None

    if self.id is not None:
      page_data = Pages._get_data(id=self.id)
    elif self.url is not None:
      page_data = Pages._get_data(url=self.url)

    if page_data is None:
      self.initialize()
    else:
      self.objetivize(page_data)



class Pages:
  PAGES = []

  KEYNAMES = ['id', 'uuid', 'url']
  FIELDNAMES = ['id', 'uuid', 'url', 'created_at', 'site', 'types', 'visited_at', 'links']

  @classmethod
  def init(cls):
    try:
      with open(PAGES_FILENAME, 'r') as f:
        cls.PAGES = json.load(f)

    except Exception as e:
      print('ERROR reading pages.json')
      print(e)

      cls.PAGES = []
      cls.commit()

  @classmethod
  def get(cls, **kwargs):
    if 'id' in kwargs:
      item_data = next((page for page in cls.PAGES if page["id"] == kwargs['id']), None)
    elif 'uuid' in kwargs:
      item_data = next((page for page in cls.PAGES if page["uuid"] == kwargs['uuid']), None)
    elif 'url' in kwargs:
      item_data = next((page for page in cls.PAGES if page["url"] == normalize_slash_url(kwargs['url'])), None)
    else:
      raise BaseException("TODO: Not implemented!")

    if item_data is None:
      return None

    item = Page(item_data)

    return item

  @classmethod
  def list(cls, **kwargs):
    item_list = []
    if 'site' in kwargs:
      item_list = (Page(page_data) for page_data in cls.PAGES if page_data["site"] == kwargs['site'])

    return item_list

  @classmethod
  def create(cls, page):
    if page.id is not None:
      page_idx = cls._get_idx(id=page.id)
      if page_idx is None:
        raise BaseException("ERROR: Not found")

      cls.PAGES[page_idx] = page.serialize()
    else:
      page_idx = cls._get_idx(url=page.url)
      if page_idx is not None:
        raise BaseException("ERROR: Duplicate")

      page.id = cls._get_next_id()

      cls.PAGES.append( page.serialize() )

    cls.commit()

  @classmethod
  def change(cls, page):
    cls.create(page)

  @classmethod
  def remove(cls, page):
    raise BaseException("TODO: Not implemented!")

  @classmethod
  def _get_next_id(cls):
    return 1+len(cls.PAGES)

  @classmethod
  def _get_idx(cls, **kwargs):
    if 'id' in kwargs:
      item = next((index for index, page in enumerate(cls.PAGES) if page["id"] == kwargs['id']), None)
      return item

    elif 'url' in kwargs:
      item = next((index for index, page in enumerate(cls.PAGES) if page["url"] == normalize_slash_url(kwargs['url'])), None)
      return item

  @classmethod
  def _get_data(cls, **kwargs):
    if 'id' in kwargs:
      item = next((page for page in cls.PAGES if page["id"] == kwargs['id']), None)
      return item

    elif 'url' in kwargs:
      item = next((page for page in cls.PAGES if page["url"] == normalize_slash_url(kwargs['url'])), None)
      return item

  @classmethod
  def commit(cls):
    with open(PAGES_FILENAME, 'w') as f:
      json.dump(cls.PAGES, f, indent=2)



Pages.init()
