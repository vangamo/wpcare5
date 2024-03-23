from flask import request
from flask_restful import Resource

SITES = [
  {
    "id": 1,
    "name": "Python site",
    "domain": "python.org",
    "homepage": "https://python.org/",
    "type": None,
    "hosting": None,
    "client": "Python software foundation",
    "created_at": "2024-03-19T11:47:35.983Z"
  },
  {
    "id": 2,
    "name": "Wordpress site",
    "domain": "wordpress.org",
    "homepage": "https://wordpress.org/",
    "type": "WP",
    "hosting": None,
    "client": "Automattic, Inc",
    "created_at": "2024-03-20T11:51:05.029Z"
  },
  {
    "id": 3,
    "name": "VanGamo page",
    "domain": "igarrido.es",
    "homepage": "https://igarrido.es/",
    "type": "Custom",
    "hosting": "Ionos",
    "client": "I. Van Gamo",
    "created_at": "2024-03-21T11:54:05.192Z"
  }
]


class Site(Resource):
  def get(self, id:int=None):
    
    if id is None:
      response = {
        "success": True,
        "info": {
          "count": len(SITES),
          "pages": 1,
          "currentPage": 0,
          "next": None,
          "prev": None
        },
        "results": SITES
      }

      return response
    else:
      item = next((site for site in SITES if site['id'] == id), None)
      if item is None:
        return { "success": False, "message": "The item was not found" }

      else:
        return { "success": True, "item": item }

  def post(self):
    response = { "success": True, "message": "The item was created successfully", "item": {"id": 4, **request.json, "created_at": "2024-03-23T12:06:46.493Z"} }

    return response

  def put(self, id:int=0):
    response = { "success": True, "message": "The item was updated successfully", "item": {} }

    return response

  def delete(self, id:int=0):
    response = { "success": True, "message": "The item was deleted successfully", "item": {} }

    return response