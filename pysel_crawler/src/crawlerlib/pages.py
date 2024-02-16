from wpcare.pages import Pages as WPCarePages
from crawlerlib.page import Page
from wpcare.jsonNamedCrud import JsonNamedCrud


class Pages(WPCarePages):
  MODEL_CLASS = Page



Pages.init()
