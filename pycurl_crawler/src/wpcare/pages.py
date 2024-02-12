from crawlerlib.crawler import Crawler
import uuid
import json
import os

ROOT_DIR = os.path.abspath(os.curdir)
DATA_DIR = os.path.join(ROOT_DIR, "data")

PAGES_FILENAME = os.path.join(DATA_DIR, "pages.json")


class Page:
  def __init__(self, url, domain=None):
    self.url = url


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

  def serialize(self):
    return {
      "uuid": str(uuid.uuid4()),
      "url": self.url,
      "type": ["landing"]
    }

  def save(self):
    page_data = self.serialize()

    print(page_data)

    with open(PAGES_FILENAME, 'w') as f:
      print(PAGES_FILENAME)
    
      json.dump(page_data, f)