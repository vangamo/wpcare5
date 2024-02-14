from wpcare.page import Page
from wpcare.utils import normalize_slash_url
from wpcare.jsonNamedCrud import JsonNamedCrud



class Pages:
  MODEL_CLASS = Page

  KEYNAMES = ['id', 'uuid', 'url']
  FIELDNAMES = ['id', 'uuid', 'url', 'created_at', 'site', 'types', 'visited_at']

  @classmethod
  def init(cls):
    cls.MODEL_CLASS.ADAPTER = cls

    cls.STORAGE = JsonNamedCrud('pages', Page, auto_commit=True, key_attr='id')



  @classmethod
  def get(cls, **kwargs):
    if 'id' in kwargs:
      item = cls.STORAGE.get( id=kwargs['id'] )
    elif 'uuid' in kwargs:
      item = cls.STORAGE.get( uuid=kwargs['uuid'] )
    elif 'url' in kwargs:
      item = cls.STORAGE.get( url=normalize_slash_url(kwargs['url']) )
    else:
      raise BaseException("TODO: Not implemented!")

    return item



  @classmethod
  def list(cls, **kwargs):
    item_list = []
    if 'site' in kwargs:
      item_list = cls.STORAGE.select( site=kwargs['site'] )

    return item_list



  @classmethod
  def create(cls, page):
    if page.id is not None:
      page_found = cls.STORAGE.get(id=page.id)

      if page_found is None:
        raise BaseException("ERROR: Not found")
      
      else:
        cls.STORAGE.update({'id': page.id}, page)

    else:
      page_found = cls.STORAGE.get(url=page.url)

      if page_found is None:
        cls.STORAGE.insert(page)
      
      else:
        cls.STORAGE.update({'url': page.url}, page)



  @classmethod
  def change(cls, page):
    cls.create(page)

  @classmethod
  def remove(cls, page):
    raise BaseException("TODO: Not implemented!")



  @classmethod
  def _get_data(cls, **kwargs):
    if 'id' in kwargs:
      item = cls.STORAGE.getRaw(id=kwargs['id'])
      return item

    elif 'url' in kwargs:
      item = cls.STORAGE.getRaw( url=normalize_slash_url(kwargs['url']) )
      return item



Pages.init()
