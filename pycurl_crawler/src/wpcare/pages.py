from wpcare.page import Page
from wpcare.utils import normalize_slash_url

import json
import os

ROOT_DIR = os.path.abspath(os.curdir)
DATA_DIR = os.path.join(ROOT_DIR, "data")

PAGES_FILENAME = os.path.join(DATA_DIR, "pages.json")



class Pages:
  MODEL_CLASS = Page
  PAGES = []

  KEYNAMES = ['id', 'uuid', 'url']
  FIELDNAMES = ['id', 'uuid', 'url', 'created_at', 'site', 'types', 'visited_at']

  @classmethod
  def init(cls):
    cls.MODEL_CLASS.ADAPTER = cls

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

    item = cls.MODEL_CLASS(item_data)

    return item

  @classmethod
  def list(cls, **kwargs):
    item_list = []
    if 'site' in kwargs:
      item_list = (cls.MODEL_CLASS(page_data) for page_data in cls.PAGES if page_data["site"] == kwargs['site'])

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
