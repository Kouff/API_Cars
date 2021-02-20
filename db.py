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

    def json(self) -> dict:
        return {
            'id': self.id,
            'vin_code': self.vin_code,
            'manufacturer': self.manufacturer,
            'model': self.model,
            'year': self.year,
            'color': self.color,
        }