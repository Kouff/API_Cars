from aiohttp import web
from db import session, engine, Base, Car


class CarListView(web.View):
    async def get(self):
        pass

    async def post(self):
        pass


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
