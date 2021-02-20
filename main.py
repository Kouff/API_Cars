import json

from aiohttp import web
from sqlalchemy.exc import IntegrityError
from db import session, engine, Base, Car


class CarListView(web.View):
    search_fields = ['manufacturer', 'model', 'color']
    year_from_field = 'year_from'
    year_to_field = 'year_to'

    async def get(self):
        query = session.query(Car)
        for field in self.search_fields:
            if field in self.request.rel_url.query:
                query = query.filter(getattr(Car, field) == self.request.rel_url.query[field])
        year_from = self.request.rel_url.query.get(self.year_from_field)
        year_to = self.request.rel_url.query.get(self.year_to_field)
        if year_from:
            query = query.filter(Car.year >= int(year_from))
        if year_to:
            query = query.filter(Car.year <= int(year_to))
        cars = query.all()
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
    async def get_car(self):
        id = self.request.match_info['id']
        car = session.query(Car).get(id)
        if not car:
            raise web.HTTPNotFound()
        return car

    async def get(self):
        car = await self.get_car()
        return web.json_response(car.json())

    async def patch(self):
        car = await self.get_car()
        data = await self.request.json()
        validated_data = await Car.check_data_to_update(data)
        for field, value in validated_data.items():
            setattr(car, field, value)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            message = {'vin_code': 'This field must be unique'}
            raise web.HTTPBadRequest(text=json.dumps(message), content_type='application/json')
        return web.json_response(car.json())

    async def delete(self):
        car = await self.get_car()
        session.delete(car)
        return web.Response(status=204)


app = web.Application()
app.add_routes([
    web.view('/cars/', CarListView),
    web.view('/cars/{id}/', CarDetailView),
])

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    web.run_app(app)
