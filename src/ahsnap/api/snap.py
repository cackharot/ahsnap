from flask import request
from flask_restful import Resource
from ..service import SnapService
import json
import logging


class SnapApi(Resource):

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.log.info('In snap api')
        self.service = SnapService()

    def get(self, _id):
        self.log.info('id=' + _id)
        return {'id': _id}

    def put(self, _id):
        self.log.info('got snaphost request')
        data = request.get_json()
        self.log.info('data=%s', json.dumps(data))
        if data.get('url') is not None:
            self.service.add(data)
        else:
            return {"error": "Invalid data given. Url is required"}, 402
        return {}, 201

    def post(self, _id):
        return None, 204

    def delete(self, _id):
        return None, 204
