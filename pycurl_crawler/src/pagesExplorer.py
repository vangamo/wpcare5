from crawlerlib.page import Page
from wpcare.utils import normalize_slash_url

LIMIT = 100
VERBOSE = True

class PagesExplorer:
  def __init__(self, url):
    self.url = url
    self.limit = LIMIT

  def set_limit(self, number):
    self.limit = number

  def visit(self):
    page = Page(self.url)
    page.addType('landing')
    page.save()

    list_pages_to_visit = [page.url]

    count = 0

    for visiting_url in list_pages_to_visit:
      if count >= self.limit:
        break
      count += 1

      visiting_page = Page(visiting_url)
      if VERBOSE: print()
      if VERBOSE: print('Visit:  ', visiting_page.url)
      visiting_page.addType('crawler')
      visiting_page.getLinks()
      visiting_page.save()

      for visited_link in visiting_page.links['navigation']['internal_pages']:
        link_url = normalize_slash_url(visited_link['normalized_href'])
        if '#' in link_url:
          link_url = link_url.split('#')[0]

        if link_url not in list_pages_to_visit:
          if VERBOSE: print('Add:    ', link_url)
          list_pages_to_visit.append(link_url)
