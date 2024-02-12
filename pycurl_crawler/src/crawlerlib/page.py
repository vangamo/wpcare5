from wpcare.page import Page as WPCarePage

from wpcare.utils import normalize_link
from crawlerlib.crawler import Crawler

from datetime import datetime
from bs4 import BeautifulSoup



def get_link_info_from_bs4(link):
  selector_path = [link.name+('#'+link['id'] if 'id' in link else '')+(''.join('.'+c for c in link.get_attribute_list('class')) if len(link.get_attribute_list('class')) > 0 and link.get_attribute_list('class')[0] is not None else '')]

  for parent in link.parents:
    selector_path.insert(0, parent.name+("#"+parent['id'] if 'id' in parent else '')+(''.join('.'+c for c in parent.get_attribute_list('class')) if len(parent.get_attribute_list('class')) > 0 and parent.get_attribute_list('class')[0] is not None else ''))

    if parent.name == 'body':
      break

  return {
    "href": link.get('href'),
    "html": str(link),
    "css_selector": selector_path
    }



class Page(WPCarePage):
  
  def __init__(self, url_or_id, domain=None):
    self.links = {
        "navigation": {
          "internal_pages": [],
          "internal_resources": [],
          "external": [],
          "other": []
        },
        "styles": [],
        "scripts": [],
        "images": []
      }

    super().__init__(url_or_id, domain)
     

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


  def serialize(self):
    parent_data = super().serialize()
    parent_data["links"] = self.links

    return parent_data

  def objetivize(self, data):
    super().objetivize(data)
    
    self.links = data['links']


