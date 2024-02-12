import pycurl
import certifi
from io import BytesIO
import re

class Crawler:
  def __init__(self, url):
    self.url = url.replace(' ', '%20').encode('iso-8859-1')
    self.headers = {}
    self.mime_type = None
    self.encoding = None


  def init_crawler(self):
    self._content_buffer = BytesIO()
    self._headers_buffer = BytesIO()
    c = pycurl.Curl()

    c.setopt(c.URL, self.url)
    c.setopt(c.WRITEDATA, self._content_buffer)
    c.setopt(c.HEADERFUNCTION, self._headers_buffer.write)
    c.setopt(c.CAINFO, certifi.where())
    c.setopt(c.FOLLOWLOCATION, True)
    #c.setopt(c.VERBOSE, True)
    #agent = "Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0"
    #c.setopt(c.USERAGENT, agent)

    return c


  def retrieve_headers_info(self):
    # Figure out what encoding was sent with the response, if any.
    # Check against lowercased header name.
    self.headers = {} # TODO
    
    (http_response, *header_lines) = self._headers_buffer.getvalue().decode('utf-8').split('\r\n')
    for header_line in header_lines:
      if header_line != '':
        (header_name, *header_value) = header_line.split(': ', maxsplit=1)
        header_name = header_name.lower()
        header_value = ''.join(header_value)
        if 'set-cookie' == header_name:
          if 'set-cookie' not in self.headers:
            self.headers['set-cookie'] = []  
          self.headers['set-cookie'].append(header_value)
        else:
          self.headers[header_name] = header_value

    self.http_response = http_response
    (http_version, response_code, response_text) = http_response.split(' ', maxsplit=2)
    self.http_version = http_version.replace('HTTP/', '')
    self.response_code = response_code
    self.response_text = ''.join(response_text)

    if 'content-type' in self.headers:
        content_type = self.headers['content-type'].lower()
        match = re.search('charset=(\S+)', content_type)
        if match:
            self.encoding = match.group(1)
            print('Decoding using %s' % self.encoding)
    if self.encoding is None:
        # Default encoding for HTML is iso-8859-1.
        # Other content types may have different default encoding,
        # or in case of binary data, may have no encoding at all.
        self.encoding = 'utf-8'
        print('Assuming encoding is %s' % self.encoding)


  def retrieve_metrics(self):
    pass # TODO


  def retrieve_content(self):
    #retrieve the content BytesIO
    self.raw_html = self._content_buffer.getvalue()


  def perform(self):
    c = self.init_crawler()

    c.perform()

    self.retrieve_headers_info()
    self.retrieve_metrics()
    self.retrieve_content()

    c.close()    


  def get_html(self, encoding = None):
    encoding = encoding or self.encoding or 'utf-8'

    return self.raw_html.decode(encoding)


if __name__ == "__main__":
  url = 'https://nucep.com'

  try:
    crawler = Crawler(url)
    crawler.perform()
    html = crawler.get_html()

    print(html)
  except Exception as e:
    print('ERROR getting ' + url)
    print(e)
