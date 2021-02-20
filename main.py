import json

from aiohttp import web
from sqlalchemy.exc import IntegrityError
from db import session, engine, Base, Car


class CarListView(web.View):
    async def get(self):
        cars = session.query(Car).all()
        return web.json_response([car.json() for car in cars])

    async def post(self):
        data = await self.request.json()
        validated_data = await Car.check_data_to_create(data)
        car = Car(**validated_data)
        session.add(car)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            message = {'vin_code': 'This field must be unique'}
            raise web.HTTPBadRequest(text=json.dumps(message), content_type='application/json')
        return web.json_response(car.json())


class CarDetailView(web.View):
    async def get(self):
        pass

    async def patch(self):
        pass

    async def delete(self):
        pass


app = web.Application()
app.add_routes([
    web.view('/cars/', CarListView),
    web.view('/cars/<id>', CarDetailView),
])

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    web.run_app(app)
