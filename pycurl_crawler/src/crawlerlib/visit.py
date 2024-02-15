from datetime import datetime

from crawlerlib.crawler import Crawler
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


class Visit():
  def __init__(self, url):
    self.url = url
    self.visited_at = None
    self.http_response = None
    self.http_version = None
    self.status_code = None
    self.status_text = None
    self.remote_ip4 = None
    self.remote_ip6 = None
    self.effective_url = url
    self.content_length = None
    self.content_type = None
    self.content_encoding = None
    self.cache_control = None
    self.cache_expires = None
    self.cache_last_modified = None
    self.cache_date = None
    self.other_headers = []

    self._crawler = None

  def perform(self):
    now = int(datetime.utcnow().timestamp())

    if self.visited_at is not None and now - self.visited_at < 60:
      print('Recent')
      return
    
    try:
      self._crawler = Crawler(self.url)
      self._crawler.perform()
      self.visited_at = now
      #html = self._crawler.get_html()

    except Exception as e:
      print('ERROR getting ' + self.url)
      print(e)
      self._crawler = None

      if e[0] == 6:
        self.status_code = e[0]
        self.status_text = e[1]
      return

    self.retrieve_response_info()
    #soup = BeautifulSoup(html, 'html.parser')
  

  def retrieve_response_info(self):
    self.http_response = self._crawler.get_http_response()
    #self.http_response = self.http_response.strip()

    (http_version, response_code, response_text) = self.http_response.split(' ', maxsplit=2)
    self.http_version = http_version # .replace('HTTP/', '')
    self.status_code = int(response_code)
    self.status_text = ' '.join(response_text)

    self.remote_ip4 = self._crawler.get_addr()
    #self.remote_ip6 = self._crawler.get_url()
    self.effective_url = self._crawler.get_url()

    headers = self._crawler.get_headers()
    print( 'VISIT.HEADERS', headers )
    if 'content-length' in headers:
      self.content_length = headers['content-length']
      del headers['content-length']

    if 'content-type' in headers:
      self.content_type = headers['content-type']
      del headers['content-type']

    self.content_encoding = self._crawler.get_encoding()

    if 'cache-control' in headers:
      self.cache_control = headers['cache-control']
      del headers['cache-control']
    
    if 'expires' in headers:
      self.cache_expires = headers['expires']
      del headers['expires']

    if 'last-modified' in headers:
      self.cache_last_modified = headers['last-modified']
      del headers['last-modified']

    if 'date' in headers:
      self.cache_date = headers['date']
      del headers['date']

    self.other_headers = list(headers.keys())

    print(vars(self))

  def get_mime_type(self):
    if self.status_code is not None and (self.status_code < 100 or self.status_code >= 300):
      return None

    if self._crawler is None:
      self.perform()

    content_type = self.content_type

    return content_type.split(';')[0]

  def get_html(self):
    if self.status_code is not None and (self.status_code < 100 or self.status_code >= 300):
      return self.status_text

    if self._crawler is None:
      self.perform()

    return self._crawler.get_html()

  def get_resources(self):
    pass

  def get_links(self):


    '''

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
