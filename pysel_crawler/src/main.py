#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pagesExplorer import PagesExplorer
from crawlerlib.pages import Pages
import sys


if __name__ == "__main__":
  url = sys.argv[1] if len(sys.argv) > 1 else 'https://python.org/'
  (protocol, void, domain, *path) = url

  explorer = PagesExplorer(url)
  explorer.set_limit(10)
  explorer.visit()

  p = Pages.get(url=url)

  print(vars(p))

  ps = Pages.list(site=domain)

  list(print(p.id, p.site, p.url, p.types) for p in ps)
