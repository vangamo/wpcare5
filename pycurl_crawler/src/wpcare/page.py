from wpcare.utils import get_site_from_url, normalize_slash_url

import uuid
from datetime import datetime
from bs4 import BeautifulSoup



class Page:
  ADAPTER = None

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
      "visited_at": self.visited_at
    }

  def objetivize(self, data):
    self.id = data['id']
    self.created_at = data["created_at"]
    self.uuid = data['uuid']
    self.url = data['url']
    self.site = data['site']
    self.types = data['types']
    self.visited_at = data['visited_at'] if 'visited_at' in data else None

  def save(self):
    self.ADAPTER.create(self)

  def load(self):
    page_data = None

    if self.id is not None:
      page_data = self.ADAPTER._get_data(id=self.id)
    elif self.url is not None:
      page_data = self.ADAPTER._get_data(url=self.url)

    if page_data is None:
      self.initialize()
    else:
      self.objetivize(page_data)
