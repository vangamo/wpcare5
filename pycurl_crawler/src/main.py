#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pagesExplorer import PagesExplorer

if __name__ == "__main__":
  url = 'https://python.org/'

  explorer = PagesExplorer(url)
  explorer.set_limit(1)
  explorer.visit()
