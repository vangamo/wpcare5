from crawlerlib.crawler import Crawler
import uuid
import json
import os

ROOT_DIR = os.path.abspath(os.curdir)
DATA_DIR = os.path.join(ROOT_DIR, "data")

PAGES_FILENAME = os.path.join(DATA_DIR, "pages.json")


def get_site_from_url(url):
  url_parts=url.split('/')

  print(url_parts)

  if url.startswith('http'):
    return url_parts[2]
  else:
    return url_parts[0]

def normalize_slash_url(url):
  # TODO: Add domain and https:

  if not url.endswith('/'):
    return url+'/'

  return url

class Page:
  def __init__(self, url, domain=None):
    self.url = url
    self.uuid = None
    self.site = ''
    self.type = []

    self.load()

  def getLinks(self):
    try:
      crawler = Crawler(self.url)
      crawler.perform()
      html = crawler.get_html()

      print(html)
    except Exception as e:
      print('ERROR getting ' + url)
      print(e)
      return []

  def initialize(self):
    self.uuid = str(uuid.uuid4())
    self.site = get_site_from_url(self.url)

  def serialize(self):
    return {
      "uuid": self.uuid,
      "url": normalize_slash_url(self.url),
      "site": self.site,
      "type": self.type
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
      json.dump(PAGES, f)

  def load(self):
    page_data = next((page for page in PAGES if page["url"] == normalize_slash_url(self.url)), None)

    if page_data is None:
      self.initialize()
    else:
      self.objetivize(page_data)

PAGES = []

with open(PAGES_FILENAME, 'r') as f:
  PAGES = json.load(f)