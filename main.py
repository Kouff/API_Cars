from aiohttp import web
from db import collection, Car


class CarListView(web.View):
    """Retrieve all the car objects or create a new car object"""
    search_fields = ['manufacturer', 'model', 'color']
    year_from_field = 'year_from'
    year_to_field = 'year_to'

    async def get_cars(self):
        filter = {}
        for field in self.search_fields:
            if field in self.request.rel_url.query:
                filter[field] = self.request.rel_url.query[field]  # add a filter
        year_from = self.request.rel_url.query.get(self.year_from_field)
        year_to = self.request.rel_url.query.get(self.year_to_field)
        if year_from and year_from.isdigit() and year_to and year_to.isdigit():
            filter['year'] = {'$gte': int(year_from), '$lte': int(year_to)}  # add a filter
        elif year_from and year_from.isdigit():
            filter['year'] = {'$gte': int(year_from)}  # add a filter
        elif year_to and year_to.isdigit():
            filter['year'] = {'$lte': int(year_to)}  # add a filter
        return [car for car in collection.find(filter, {'_id': 0})]

    async def get(self):
        cars = await self.get_cars()  # get cars
        return web.json_response(cars)

    async def post(self):
        data = await self.request.json()  # get data
        validated_data = await Car.check_data_to_create(data)  # check the data
        collection.insert_one(validated_data.copy())
        # del validated_data['_id']
        return web.json_response(validated_data)


class CarDetailView(web.View):
    """Retrieve, update and delete a car object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vin_code = self.request.match_info['vin_code']  # get id from url

    async def get(self):
        car = collection.find_one({'vin_code': self.vin_code}, {'_id': 0})  # get a car
        if not car:
            raise web.HTTPNotFound()  # send a response with status 404 if the car is not found
        return web.json_response(car)

    async def patch(self):
        data = await self.request.json()  # get data
        validated_data = await Car.check_data_to_update(data, self.vin_code)  # check the data
        # get and update the car fields
        car = collection.find_one_and_update({'vin_code': self.vin_code}, {'$set': validated_data})
        if car is None:
            raise web.HTTPNotFound()  # send a response with status 404 if the car is not found
        del car['_id']
        car.update(validated_data)
        return web.json_response(car)

    async def delete(self):
        car = collection.find_one_and_delete({'vin_code': self.vin_code})  # delete the car
        if car is None:
            raise web.HTTPNotFound()  # send a response with status 404 if the car is not found
        return web.Response(status=204)


app = web.Application()
app.add_routes([
    web.view('/cars/', CarListView),
    web.view('/cars/{vin_code}/', CarDetailView),
])

if __name__ == '__main__':
    web.run_app(app)
