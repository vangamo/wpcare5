#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wpcare.pages import Page


if __name__ == "__main__":
  url = 'https://nucep.com'

  page = Page(url)
  #page.getLinks()

  page.save()
