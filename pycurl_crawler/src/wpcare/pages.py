from crawlerlib.crawler import Crawler

from bs4 import BeautifulSoup

import uuid
import json
import os

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
  def __init__(self, url, domain=None):
    self.url = normalize_slash_url(url)
    self.uuid = None
    self.site = ''
    self.type = []

    self.load()

  def getLinks(self):
    try:
      crawler = Crawler(self.url)
      crawler.perform()
      html = crawler.get_html()

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
        "links": links,
        "styles":  [link.get('src') for link in soup.find_all('link') if link.get('src') is not None and link.get('src') != '' ],
        "scripts":  [link.get('src') for link in soup.find_all('script') if link.get('src') is not None and link.get('src') != '' ],
        "images":  [link.get('src') for link in soup.find_all('img') if link.get('src') is not None and link.get('src') != '' ]
    }

  def initialize(self):
    self.uuid = str(uuid.uuid4())
    self.site = get_site_from_url(self.url)

  def serialize(self):
    return {
      "uuid": self.uuid,
      "url": normalize_slash_url(self.url),
      "site": self.site,
      "type": self.type,
      "links": self.links
    }

  def objetivize(self, data):
    self.uuid = data['uuid']
    self.site = data['site']
    self.type = data['type']

  def save(self):
    page_index = next((index for index, page in enumerate(PAGES) if page["url"] == self.url), None)
    page_data = self.serialize()

    if page_index is None:
      PAGES.append(page_data)
    else:
      PAGES[page_index] = page_data

    with open(PAGES_FILENAME, 'w') as f:
      json.dump(PAGES, f, indent=2)

  def load(self):
    page_data = next((page for page in PAGES if page["url"] == normalize_slash_url(self.url)), None)

    if page_data is None:
      self.initialize()
    else:
      self.objetivize(page_data)

PAGES = []

with open(PAGES_FILENAME, 'r') as f:
  PAGES = json.load(f)