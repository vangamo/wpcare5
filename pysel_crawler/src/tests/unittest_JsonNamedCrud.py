import unittest

from crawlerlib.page import Page
from wpcare.jsonNamedCrud import JsonNamedCrud

testCrud = JsonNamedCrud('test-page', Page, auto_commit=False)

class Test_JsonNamedCrud(unittest.TestCase):
  def test_insert(self):
    data = {
      "created_at": 1707764259,
      "uuid": "b9e58e6a-7217-406c-805a-259f692fbf20",
      "url": "https://realpython.com/python-testing/",
      "site": "realpython.com",
      "types": [
        "landing",
        "crawler"
      ],
      "visited_at": 1707765225,
      "links": {
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
    }
    testCrud.insert(data)

    result = testCrud.get(id=1)
    self.assertEqual(result, data)

if __name__ == "__main__":
  unittest.main()
  