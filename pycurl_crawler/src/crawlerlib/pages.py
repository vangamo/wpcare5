from wpcare.pages import Pages as WPCarePages
from crawlerlib.page import Page


class Pages(WPCarePages):
  MODEL_CLASS = Page
  PAGES = []

  KEYNAMES = ['id', 'uuid', 'url']
  FIELDNAMES = ['id', 'uuid', 'url', 'created_at', 'site', 'types', 'visited_at', 'links']


Pages.init()
