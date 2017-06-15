from flask import Flask, request
from flask_restful import Api

import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
api = Api(app)

@app.route('/')
def home():
    return "Welcome", 200

from .api import SnapApi

api.add_resource(SnapApi, '/api/snap/<string:_id>')

if __name__ == '__main__':
    app.run(debug=True)
