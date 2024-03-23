from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

@app.route('/')
def get_root():
  return 'Oh oh', 404

@app.route('/api/')
def get_api_root():
  return 'Site not created', 404

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5000)