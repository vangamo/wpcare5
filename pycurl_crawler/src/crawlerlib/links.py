from wpcare.jsonNamedCrud import JsonNamedCrud
#from wpcare.jsonCrud import JsonCrud

class Link():
  ADAPTER = None

  def __init__(self, data):
    self.id = data['id'] if 'id' in data else None
    self.href = data['href']
    self.normalized_href = data['normalized_href']
    self.type = data['type']
    self.html = data['html']
    self.css_selector = data['css_selector']
    #self.path_selector = data['path_selector']
    self.page_referrer = data['page_referrer']

  def serialize(self):
    return {
      "id": self.id,
      "href": self.href,
      "normalized_href": self.normalized_href,
      'type': self.type,
      "html": self.html,
      "css_selector": self.css_selector,
      #"path_selector": self.path_selector,
      "page_referrer": self.page_referrer,
    }

class Links():
  MODEL_CLASS = Link

  @classmethod
  def init(cls):
    cls.MODEL_CLASS.ADAPTER = cls
    cls.STORAGE = JsonNamedCrud('page-links', cls.MODEL_CLASS, auto_commit=True, key_attr='id')
    #cls.STORAGE = JsonCrud('page-links', auto_commit=True, key_attr='id')

  @classmethod
  def get(cls, **kwargs):
    raise BaseException("TODO: Not implemented!")

  @classmethod
  def list(cls, **kwargs):
    raise BaseException("TODO: Not implemented!")

  @classmethod
  def create(cls, item):
    if item.id is not None:
      item_found = cls.STORAGE.get(id=item.id)

      if item_found is None:
        raise BaseException("ERROR: Not found")
      
      else:
        cls.STORAGE.update({'id': item.id}, item)

    else:
      item_found = cls.STORAGE.get(href=item.href)

      if item_found is None:
        cls.STORAGE.insert(item)
      
      else:
        cls.STORAGE.update({'href': item.href}, item)

  @classmethod
  def change(cls, page):
    raise BaseException("TODO: Not implemented!")

  @classmethod
  def remove(cls, page):
    raise BaseException("TODO: Not implemented!")

  @classmethod
  def _get_data_raw(cls, **kwargs):
    raise BaseException("TODO: Not implemented!")



Links.init()