from wpcare.page import Page as WPCarePage

from wpcare.utils import normalize_link # Remove
from crawlerlib.crawler import Crawler

from datetime import datetime # Remove
from bs4 import BeautifulSoup # Remove



def get_link_info_from_bs4(link): # Remove
  selector_path = [link.name+('#'+link['id'] if 'id' in link else '')+(''.join('.'+c for c in link.get_attribute_list('class')) if len(link.get_attribute_list('class')) > 0 and link.get_attribute_list('class')[0] is not None else '')]

  for parent in link.parents:
    selector_path.insert(0, parent.name+("#"+parent['id'] if 'id' in parent else '')+(''.join('.'+c for c in parent.get_attribute_list('class')) if len(parent.get_attribute_list('class')) > 0 and parent.get_attribute_list('class')[0] is not None else ''))

    if parent.name == 'body':
      break

  return {
    "href": link.get('href'),
    "html": str(link),
    "css_selector": selector_path,
    "page_referrer": None,
    "type": None
    }



class Page(WPCarePage):
  FIELDNAMES = ['id', 'uuid', 'url', 'created_at', 'site', 'types', 'visited_at', 'links', "status_code"]
  KEYS = ['id', 'uuid', 'url']
  
  def __init__(self, url_or_id):
    super().__init__(url_or_id)

    if not hasattr(self, 'visited_at'):
      self.visited_at = None

    if not hasattr(self, 'links'):  
      self.links = None

     

  def add_visit(self, visit):
    self.last_visit = visit
    html = visit.get_html()

    self.url = visit.effective_url

    self.analyze_html(html)


  def analyze_html(self, html):
    soup = BeautifulSoup(html, 'html.parser')
    links = self.find_navigation_links(soup)

  def find_navigation_links(self, soup):
    self.links = [get_link_info_from_bs4(link) for link in soup.find_all('a') if link.get('href') is not None and link.get('href') != '' ]

  def get_links(self):
    return self.links

  '''
    self.find_internal_links(all_links)

  def find_internal_links(self, all_links):
    self.links_internal = []
    
    print('NUM LINKS', len(all_links))

    index = 0
    while index < len(all_links):
      link = all_links[index]
      normalized_link = normalize_link(link['href'], self.url)
      link['normalized_href'] = normalized_link


      #' ' '
      #elif normalized_link.startswith('http:') or normalized_link.startswith('https:'):
      #  links['external'].append(link)
      #else:
      #  links['other'].append(link)
      #' ' '
   
  '''

  '''
  def getLinks(self):
    now = int(datetime.utcnow().timestamp())

    if self.visited_at is not None and now - self.visited_at < 60:
      print('Recent')
      return

    try:
      crawler = Crawler(self.url)
      crawler.perform()
      html = crawler.get_html()
      self.visited_at = now

    except Exception as e:
      print('ERROR getting ' + url)
      print(e)
      return []

    soup = BeautifulSoup(html, 'html.parser')

    # Links

    all_links = [get_link_info_from_bs4(link) for link in soup.find_all('a') if link.get('href') is not None and link.get('href') != '' ]

    links = {
      "internal_pages": [],
      "internal_resources": [],
      "external": [],
      "other": []
    }

    # TODO: Links starts with //

    for link in all_links:
      normalized_link = normalize_link(link['href'], self.url)
      link['normalized_href'] = normalized_link

      if normalized_link.startswith('/'):
        links['internal_pages'].append(link)
      elif normalized_link.startswith('#'):
        links['internal_pages'].append(link)
      elif normalized_link.startswith(self.site) or normalized_link.startswith('http://'+self.site) or normalized_link.startswith('https://'+self.site):
        links['internal_pages'].append(link)
      elif normalized_link.startswith('http:') or normalized_link.startswith('https:'):
        links['external'].append(link)
      else:
        links['other'].append(link)

    self.links = {
        "navigation": links,
        "styles":  [link.get('src') for link in soup.find_all('link') if link.get('src') is not None and link.get('src') != '' ],
        "scripts":  [link.get('src') for link in soup.find_all('script') if link.get('src') is not None and link.get('src') != '' ],
        "images":  [link.get('src') for link in soup.find_all('img') if link.get('src') is not None and link.get('src') != '' ]
    }
  '''

  def serialize(self):
    parent_data = super().serialize()
    parent_data["visited_at"] = self.visited_at
    #parent_data["links"] = self.links # Don't save it into pages storage

    return parent_data

  def objetivize(self, data):
    super().objetivize(data)

    self.visited_at = data['visited_at'] if 'visited_at' in data else None
    #self.links = data['links'] if 'links' in data else [] # TODO: Don't retrieve it from pages storage
