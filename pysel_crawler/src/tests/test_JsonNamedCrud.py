import sys
import os
print(os.path.dirname(os.path.realpath(__file__)) + "/..")
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

'''
Note: What if your application is a single script?

You can import any attributes of the script, such as classes, functions, and variables by using the built-in __import__() function. Instead of from my_sum import sum, you can write the following:

target = __import__("my_sum.py")
sum = target.sum

The benefit of using __import__() is that you don’t have to turn your project folder into a package, and you can specify the file name. This is also useful if your filename collides with any standard library packages. For example, math.py would collide with the math module.
'''

#crawlerlib_page = __import__("crawlerlib.page")
#Page = crawlerlib_page.Page
#wpcare_jsonNamedCrud = __import__("..wpcare.jsonNamedCrud")
#JsonNamedCrud = wpcare_jsonNamedCrud.JsonNamedCrud

from crawlerlib.page import Page
from wpcare.jsonNamedCrud import JsonNamedCrud

testCrud = JsonNamedCrud('test-page', Page, auto_commit=False)

class TestJsonNamedCrud():

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
    assert result.serialize() == data