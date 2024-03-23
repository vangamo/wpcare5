from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from controllers.sites import Site

app = Flask(__name__)
api = Api(app)
CORS(app)

@app.route('/')
def get_root():
  return 'Oh oh', 404

@app.route('/api/')
def get_api_root():
  return 'Site not created', 404

api.add_resource(Site, "/api/sites/", "/api/site/", "/api/site/<int:id>", "/api/site/<int:id>/")



if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5000)