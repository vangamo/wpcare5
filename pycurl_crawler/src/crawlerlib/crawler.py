from datetime import datetime
import time
import os
from random import random
import atexit

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.chrome.options import Options


class Crawler:
  driver = None
  last_use = 0

  @classmethod
  def get_driver(cls):
    now = int(datetime.utcnow().timestamp())

    if cls.driver is None:
      options = Options()
      options.add_argument("--headless")

      cls.driver = webdriver.Firefox(options=options)

      atexit.register(cls.close)

    if now - cls.last_use < 1000:
      time.sleep(random()*9)

    return cls.driver
  


  @classmethod
  def close(cls):
    print('Closing')
    cls.driver.close()



  def __init__(self, url):
    self.url = url.replace(' ', '%20')
    self.headers = {}
    self.content_type = None
    self.encoding = None
    self.addr = None
    self.effective_url = None
    self.http_response = None


  def init_crawler(self):
    #options = Options()
    #options.add_argument("--headless")
    #driver = webdriver.Firefox(options=options)
    #driver = webdriver.Firefox(options=options, service_log_path=os.devnull)  # Avoid log file

    #chromeOptions = Options()
    #chromeOptions.add_argument("--headless=new")
    #driver = webdriver.Chrome(options=chromeOptions, keep_alive=False)

    return Crawler.get_driver()


  def retrieve_headers_info(self, driver):
    # Figure out what encoding was sent with the response, if any.
    # Check against lowercased header name.
    #self.headers = {} # TODO
         
    #self.http_response = http_response
    
    #self.content_type = self.headers['content-type'].lower()
    #self.encoding is None:

    self.http_response = 'HTTP/1.2 200 Ok'
    self.encoding = driver.execute_script("return document.characterSet || document.charset").lower()
    self.content_type = driver.execute_script("return document.contentType")+'; '+self.encoding
    self.headers = {
      'content-type': self.content_type
    }

    self.effective_url = driver.execute_script("return window.location.href")
    


  def retrieve_metrics(self):
    pass # TODO


  def retrieve_content(self, driver):
    #retrieve the content BytesIO
    #self.raw_html = driver.execute_script("return document.documentElement.outerHTML")
    #self.raw_html = driver.execute_async_script()
    self.raw_html = driver.execute_script("return document.documentElement.outerHTML")
    


  def perform(self):
    driver = self.init_crawler()

    driver.get(self.url)

    self.addr = 'IP'
    self.effective_url = ''

    self.retrieve_headers_info(driver)
    self.retrieve_metrics()
    self.retrieve_content(driver)

    #driver.quit()


  def get_html(self, encoding = None):
    #encoding = encoding or self.encoding or 'utf-8'

    #return self.raw_html.decode(encoding)

    return self.raw_html
  
  def get_headers(self):
    return self.headers

  def get_http_response(self):
    return self.http_response

  def get_encoding(self):
    return self.encoding

  def get_addr(self):
    return self.addr
  
  def get_url(self):
    return self.effective_url

if __name__ == "__main__":
  url = 'https://python.org/'
  url = 'https://books.adalab.es/materiales-del-curso-a-pt/'

  crawler = Crawler(url)
  crawler.perform()
  html = crawler.get_html()
  print(html)

  #try:
  #  crawler = Crawler(url)
  #  crawler.perform()
  #  html = crawler.get_html()
  #
  #  print(html)
  #except Exception as e:
  #  print('ERROR getting ' + url)
  #  print(e)
