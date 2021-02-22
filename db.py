import json
import os

from aiohttp import web
from pymongo import MongoClient

client = MongoClient(
    f'mongodb://{os.environ.get("MONGO_INITDB_ROOT_USERNAME")}:{os.environ.get("MONGO_INITDB_ROOT_PASSWORD")}@{os.environ.get("MONGODB_HOSTNAME")}/'
)
db = client[os.environ.get("MONGO_INITDB_DATABASE")]
collection = db['cars']


class Car:
    fields = {'vin_code': str, 'manufacturer': str, 'model': str, 'year': int, 'color': str}

    @classmethod
    async def check_data_to_create(cls, data: dict) -> dict:
        messages = {}
        vin_codes = [element['vin_code'] for element in collection.find({}, {'_id': 0, 'vin_code': 1})]
        for field, field_type in cls.fields.items():
            if field in data:
                if not isinstance(data[field], field_type):
                    messages[field] = f'This field must be {field_type.__name__}'
            else:
                messages[field] = f'This field is required'
        if data['vin_code'] in vin_codes:
            messages['vin_code'] = 'This field must be unique'
        if messages:
            raise web.HTTPBadRequest(text=json.dumps(messages), content_type='application/json')
        return {field: data[field] for field in Car.fields}

    @classmethod
    async def check_data_to_update(cls, data: dict, old_vin_code) -> dict:
        messages = {}
        for field, field_type in cls.fields.items():
            if field in data and not isinstance(data[field], field_type):
                messages[field] = f'This field must be {field_type.__name__}'
        new_vin_code = data.get('vin_code')
        if new_vin_code and new_vin_code != old_vin_code:
            vin_codes = [element['vin_code'] for element in collection.find({}, {'_id': 0, 'vin_code': 1})]
            if new_vin_code in vin_codes:
                messages['vin_code'] = 'This field must be unique'
        if messages:
            raise web.HTTPBadRequest(text=json.dumps(messages), content_type='application/json')
        return {key: data[key] for key in data if key in cls.fields}
