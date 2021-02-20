import json

from aiohttp import web
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db.sqlite', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Car(Base):
    __tablename__ = "cars"
    fields = {'vin_code': str, 'manufacturer': str, 'model': str, 'year': int, 'color': str}
    id = Column(Integer, primary_key=True)
    vin_code = Column(String, unique=True)
    manufacturer = Column(String)
    model = Column(String)
    year = Column(Integer)
    color = Column(String)

    @classmethod
    async def check_data_to_create(cls, data: dict) -> dict:
        messages = {}
        for field, field_type in cls.fields.items():
            if field in data:
                if not isinstance(data[field], field_type):
                    messages[field] = f'This field must be {field_type.__name__}'
            else:
                messages[field] = f'This field is required'
        if messages:
            raise web.HTTPBadRequest(text=json.dumps(messages), content_type='application/json')
        return {field: data[field] for field in Car.fields}

    def json(self) -> dict:
        return {
            'id': self.id,
            'vin_code': self.vin_code,
            'manufacturer': self.manufacturer,
            'model': self.model,
            'year': self.year,
            'color': self.color,
        }