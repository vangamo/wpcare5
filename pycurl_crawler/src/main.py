from crawlerlib.crawler import Crawler


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