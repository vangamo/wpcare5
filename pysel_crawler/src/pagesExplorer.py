from crawlerlib.page import Page
from crawlerlib.visit import Visit, Visits
from crawlerlib.links import Link, Links

from wpcare.utils import normalize_slash_url # Remove?
from wpcare.utils import normalize_link


LIMIT = 100
VERBOSE = True


def are_same_domain(url_a, url_b):
  return url_a.startswith(url_b) or url_a.startswith('http://'+url_b) or url_a.startswith('https://'+url_b)


class PagesExplorer:
  def __init__(self, url):
    self.url = url
    self.limit = LIMIT

  def set_limit(self, number):
    self.limit = number

  def visit(self):
    list_url_to_visit = [self.url]
    
    page = Page(self.url)
    page.addType('landing')
    page.save()

    count = 0

    for visiting_url in list_url_to_visit:
      if count >= self.limit:
        break
      count += 1

      new_links = self.visit_url(visiting_url)

      for link_url in new_links:

        if '#' in link_url:
          link_url = link_url.split('#')[0]

        if link_url not in list_url_to_visit:
          if VERBOSE: print('  - Push:    ', link_url)
          list_url_to_visit.append(link_url)



  def visit_url(self, visiting_url):
    if VERBOSE: print()
    if VERBOSE: print('VISITING', visiting_url)

    # TODO: Visit url or visit effective_url must be key?

    visited_link = Visits.list(url=visiting_url)

    try:
      *_, visited_link = visited_link  # last item (like .pop() for generators)

    except:
      # No elements, create one
      visited_link = Visit( visiting_url )

    mime = visited_link.get_mime_type()

    if VERBOSE and visiting_url != visited_link.effective_url:
      print('  - Correct URL: ', visiting_url, '->', visited_link.effective_url)
    if VERBOSE: print('  - Has mime:', mime)

    if mime == 'text/html':
      new_links = self.visit_page(visiting_url, visited_link)
      return new_links

    # TODO: Check for images, media, pdf,...

    return []



  def visit_page(self, visiting_url, visited_link):
    if not are_same_domain(visited_link.effective_url, self.url):
      return []
    
    visited_page = Page(visited_link.effective_url)  # TODO: Ignore query_params? and #?
    visited_page.addType('crawler')
    visited_page.add_visit(visited_link)
    visited_page.save()

    new_links = []

    links_to_visit = visited_page.get_links()

    if VERBOSE: print('  - Links to visit:', len(links_to_visit))
    new_menu_links = self.find_menu_links(visited_page, links_to_visit)
    new_links.extend(new_menu_links)
    if VERBOSE: print('  - Links to visit:', len(links_to_visit))
    new_internal_links = self.find_internal_links(visited_page, links_to_visit)
    new_links.extend(new_internal_links)
    if VERBOSE: print('  - Links to visit:', len(links_to_visit))
    if VERBOSE: list(print(l['href']) for l in links_to_visit)
    

    return new_links



  def find_internal_links(self, visited_page, links_to_visit):
    if VERBOSE: print('  - FIND INTERNAL LINKS:')
    internal_link_urls = []
    index = 0

    while index < len(links_to_visit):
      link = links_to_visit[index]
      normalized_link = normalize_link(link['href'], visited_page.url)
      link['normalized_href'] = normalized_link

      if are_same_domain(normalized_link, visited_page.site):
        if VERBOSE: print('    - Add internal', normalized_link)
        internal_link_urls.append(normalized_link)

        link['page_referrer'] = visited_page.url
        link['type'] = 'internal'

        Links.create(Link(link))

        del links_to_visit[index]
      else:
        index += 1

    return internal_link_urls
  

  def find_menu_links(self, visited_page, links_to_visit):
    if VERBOSE: print('  - FIND MENU LINKS:')
    menu_link_urls = []
    index = 0

    while index < len(links_to_visit):
      link = links_to_visit[index]
      normalized_link = normalize_link(link['href'], visited_page.url)
      link['normalized_href'] = normalized_link

      path_selector = ' > '.join(link['css_selector'])
      
      if '.elementor-nav-menu' in path_selector:

        if are_same_domain(normalized_link, visited_page.site):
          if VERBOSE: print('    - Add menu internal', normalized_link)
          menu_link_urls.append(normalized_link)

          link['page_referrer'] = visited_page.url
          link['type'] = 'menu,internal'

          Links.create(Link(link))

          del links_to_visit[index]

        else:
          if VERBOSE: print('    - Add menu external', normalized_link)
          menu_link_urls.append(normalized_link)

          link['page_referrer'] = visited_page.url
          link['type'] = 'menu,external'

          Links.create(Link(link))

          del links_to_visit[index]

      else:
        index += 1

    return menu_link_urls