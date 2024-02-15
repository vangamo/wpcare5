from wpcare.base import ModelBase
from wpcare.base import AdapterBase



class Link(ModelBase):
  FIELDNAMES = ['id', 'created_at', 'href', 'normalized_href', 'type', 'html', 'css_selector', 'page_referrer']
  KEYS = ['id']


  def __init__(self, id_or_data):
    super().__init__(id_or_data)

    if isinstance(id_or_data, dict):
      self.id = id_or_data['id'] if 'id' in id_or_data else None
      self.href = id_or_data['href']
      self.normalized_href = id_or_data['normalized_href']
      self.type = id_or_data['type']
      self.html = id_or_data['html']
      self.css_selector = id_or_data['css_selector']
      self.page_referrer = id_or_data['page_referrer']

  def serialize(self):
    return {
      "id": self.id,
      "href": self.href,
      "normalized_href": self.normalized_href,
      'type': self.type,
      "html": self.html,
      "css_selector": self.css_selector,
      "page_referrer": self.page_referrer,
    }



class Links(AdapterBase):
  MODEL_CLASS = Link
  NAME = 'page-links'



Links.init()