from application import db
from flask_login import UserMixin
from datetime import datetime
import pandas as pd


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    model = db.Column(db.String(255))
    transmission = db.Column(db.String(255))
    mileage = db.Column(db.Integer)
    fuelType = db.Column(db.String(255))
    tax = db.Column(db.Integer)
    mpg = db.Column(db.Integer)
    engineSize = db.Column(db.Float)
    brand = db.Column(db.String(255))
    price = db.Column(db.Float)

    def __init__(
        self,
        year,
        model,
        transmission,
        mileage,
        fuelType,
        tax,
        mpg,
        engineSize,
        brand,
        price,
    ):
        self.year = year
        self.model = model
        self.transmission = transmission
        self.mileage = mileage
        self.fuelType = fuelType
        self.tax = tax
        self.mpg = mpg
        self.engineSize = engineSize
        self.brand = brand
        self.price = price


class Wishlist(db.Model):
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), primary_key=True, nullable=False
    )
    car_id = db.Column(
        db.Integer, db.ForeignKey("car.id"), primary_key=True, nullable=False
    )
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, user_id, car_id):
        self.user_id = user_id
        self.car_id = car_id


class History(db.Model):
    histID = db.Column(db.Integer, primary_key=True, nullable=False)
    id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    year = db.Column(db.Integer)
    transmission = db.Column(db.String(255))
    mileage = db.Column(db.Integer)
    fuelType = db.Column(db.String(255))
    tax = db.Column(db.Integer)
    mpg = db.Column(db.Integer)
    engineSize = db.Column(db.Float)
    brand = db.Column(db.String(255))
    price = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(
        self,
        id,
        year,
        transmission,
        mileage,
        fuelType,
        tax,
        mpg,
        engineSize,
        brand,
        price,
    ):
        self.id = id
        self.year = year
        self.transmission = transmission
        self.mileage = mileage
        self.fuelType = fuelType
        self.tax = tax
        self.mpg = mpg
        self.engineSize = engineSize
        self.brand = brand
        self.price = price


def populate_cars():
    if Car.query.first() is None:
        hdf5_file = "./model/cars.h5"
        df = pd.read_hdf(hdf5_file, key="cars")
        data_to_insert = df.to_dict(orient="records")
        db.session.bulk_insert_mappings(Car, data_to_insert)
        db.session.commit()
    pass
