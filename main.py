import json

from aiohttp import web
from sqlalchemy.exc import IntegrityError
from db import session, engine, Base, Car


class CarListView(web.View):
    """Retrieve all the car objects or create a new car object"""
    search_fields = ['manufacturer', 'model', 'color']
    year_from_field = 'year_from'
    year_to_field = 'year_to'

    async def get_cars(self):
        query = session.query(Car)
        for field in self.search_fields:
            if field in self.request.rel_url.query:
                query = query.filter(
                    getattr(Car, field) == self.request.rel_url.query[field])  # add a filter to query
        year_from = self.request.rel_url.query.get(self.year_from_field)
        year_to = self.request.rel_url.query.get(self.year_to_field)
        if year_from:
            query = query.filter(Car.year >= int(year_from))  # add a filter to query
        if year_to:
            query = query.filter(Car.year <= int(year_to))  # add a filter to query
        return query.all()

    async def get(self):
        cars = await self.get_cars()  # get cars
        return web.json_response([car.json() for car in cars])

    async def post(self):
        data = await self.request.json()  # get data
        validated_data = await Car.check_data_to_create(data)  # check the data
        car = Car(**validated_data)  # create a car instance
        session.add(car)  # add the car instance to db
        try:
            session.commit()  # send to db
        except IntegrityError:
            session.rollback()
            message = {'vin_code': 'This field must be unique'}
            raise web.HTTPBadRequest(text=json.dumps(message),
                                     content_type='application/json')  # send a response with a message
        return web.json_response(car.json())


class CarDetailView(web.View):
    """Retrieve, update and delete a car object"""

    async def get_car(self):
        id = self.request.match_info['id']  # get id from url
        car = session.query(Car).get(id)  # get a car
        if not car:
            raise web.HTTPNotFound()  # send a response with status 404 if the car is not found
        return car

    async def get(self):
        car = await self.get_car()  # get a car
        return web.json_response(car.json())

    async def patch(self):
        car = await self.get_car()  # get a car
        data = await self.request.json()  # get data
        validated_data = await Car.check_data_to_update(data)  # check the data
        for field, value in validated_data.items():
            setattr(car, field, value)  # update the car fields
        try:
            session.commit()  # send to db
        except IntegrityError:
            session.rollback()
            message = {'vin_code': 'This field must be unique'}
            raise web.HTTPBadRequest(
                text=json.dumps(message), content_type='application/json')  # send a response with a message
        return web.json_response(car.json())

    async def delete(self):
        car = await self.get_car()  # get a car
        session.delete(car)  # delete the car
        return web.Response(status=204)


app = web.Application()
app.add_routes([
    web.view('/cars/', CarListView),
    web.view('/cars/{id}/', CarDetailView),
])

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    web.run_app(app)
