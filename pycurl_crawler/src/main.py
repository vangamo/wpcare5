#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pagesExplorer import PagesExplorer
from wpcare.pages import Pages


if __name__ == "__main__":
  url = 'https://python.org/'

  explorer = PagesExplorer(url)
  #explorer.set_limit(1)
  explorer.visit()

  p = Pages.get(url='https://www.lupescoto.com/')

  print(vars(p))

  ps = Pages.list(site='www.lupescoto.com')

  list(print(p.id, p.site, p.url) for p in ps)