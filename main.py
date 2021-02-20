from aiohttp import web
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine

engine = create_engine('sqlite:///db.sqlite', echo=True)
Base = declarative_base()


class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True)
    vin_code = Column(String, unique=True)
    manufacturer = Column(String)
    model = Column(String)
    year = Column(Integer)
    color = Column(String)


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
    web.view('cars/', CarListView),  # POST GET
    web.view('cars/<id>', CarDetailView),  # GET PATCH DELETE
])

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    web.run_app(app)
