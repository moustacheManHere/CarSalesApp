from application.models import *
from application.database import *
from application.ml import *
from application.forms import * 
from application.auth import *
from flask_login import current_user


def test_user_init():
    test_user = User(name='Test User', email='test@example.com', password='password')
    assert test_user is not None
    assert test_user.name == 'Test User'
    assert test_user.email == 'test@example.com'
    assert test_user.password == 'password'

def test_car_init():
    test_car = Car(
        year=7,
        model='Test Model',
        transmission='Automatic',
        mileage=5000,
        fuelType='Petrol',
        tax=100,
        mpg=25,
        engineSize=2.0,
        brand='Audi',
        price=25000.0,
    )
    assert test_car is not None
    assert test_car.year == 7
    assert test_car.model == 'Test Model'
    assert test_car.transmission == 'Automatic'
    assert test_car.mileage == 5000
    assert test_car.fuelType == 'Petrol'
    assert test_car.tax == 100
    assert test_car.mpg == 25
    assert test_car.engineSize == 2.0
    assert test_car.brand == 'Audi'
    assert test_car.price == 25000.0

def test_wishlist_init():
    test_wishlist = Wishlist(user_id=1, car_id=2)
    assert test_wishlist is not None
    assert test_wishlist.user_id == 1
    assert test_wishlist.car_id == 2

def test_history_init():
    test_history = History(
        id=1,
        year=7,
        transmission='Automatic',
        mileage=5000,
        fuelType='Petrol',
        tax=100,
        mpg=25,
        engineSize=2.0,
        brand='Audi',
        price=25000.0,
    )
    assert test_history is not None
    assert test_history.id == 1
    assert test_history.year == 7
    assert test_history.transmission == 'Automatic'
    assert test_history.mileage == 5000
    assert test_history.fuelType == 'Petrol'
    assert test_history.tax == 100
    assert test_history.mpg == 25
    assert test_history.engineSize == 2.0
    assert test_history.brand == 'Audi'
    assert test_history.price == 25000.0

def test_populate_cars(db):
    assert Car.query.count() > 0
    assert Car.query.filter_by(brand='audi').count() > 0
    sample_car = Car.query.first()
    assert sample_car.brand is not None
    assert sample_car.model is not None
    assert sample_car.year is not None
    assert sample_car.transmission is not None
    assert sample_car.mileage is not None
    assert sample_car.fuelType is not None
    assert sample_car.tax is not None
    assert sample_car.mpg is not None
    assert sample_car.engineSize is not None
    assert sample_car.price is not None

def test_user_init():
    test_user = User(name='Test User', email='test@example.com', password='password')
    assert test_user is not None
    assert test_user.name == 'Test User'
    assert test_user.email == 'test@example.com'
    assert test_user.password == 'password'

def test_user_add_remove(db):
    test_user = User(name='Test User', email='test2@example.com', password='password')
    user_id = add_entry(test_user)
    
    retrieved_user = User.query.filter_by(id=user_id).first()

    assert retrieved_user is not None
    assert retrieved_user.name == 'Test User'
    assert retrieved_user.email == 'test2@example.com'
    assert retrieved_user.password == 'password'

    remove_entry(user_id, User)
    
    retrieved_user = User.query.filter_by(id=user_id).first()
    assert retrieved_user is None


def test_history_add_remove(app,db):
    with app.test_request_context("/"):
        data = User.query.first()
        if data is None:
            print("no users")
            return
        user_id = data.id
        test_history = History(
            id=user_id,
            year=2022,
            transmission='Automatic',
            mileage=12000,
            fuelType='Petrol',
            tax=150,
            mpg=25,
            engineSize=1.8,
            brand='Audi',
            price=20000
        )

        history_id = add_history(test_history)

        retrieved_history = History.query.filter_by(histID=history_id).first()

        assert retrieved_history is not None
        assert retrieved_history.id == user_id
        assert retrieved_history.year == 2022
        assert retrieved_history.transmission == 'Automatic'
        assert retrieved_history.mileage == 12000
        assert retrieved_history.fuelType == 'Petrol'
        assert retrieved_history.tax == 150
        assert retrieved_history.mpg == 25
        assert retrieved_history.engineSize == 1.8
        assert retrieved_history.brand == 'Audi'
        assert retrieved_history.price == 20000

        remove_entry(history_id, History)

        retrieved_history = History.query.filter_by(histID=history_id).first()
        assert retrieved_history is None
        remove_entry(user_id, User)

def test_regression_model(app):
    with app.test_request_context("/"):
        model = RegressionModel()
        assert model is not None
        valid_form = NewRegressionForm(
            year=5, transmission='Manual', mileage=50000, fuelType='Petrol',
            tax=200, mpg=30.5, engineSize=2.0, brand='audi'
        )
        assert valid_form is not None
        prediction = model.predict(valid_form)
        assert prediction is not None
        assert isinstance(prediction, float)


def test_check_login(app):
    with app.test_request_context("/"):
        data = User.query.first()
        if data is None:
            print("no users")
            return
        valid_login_form = LoginForm(email=data.email, password=data.password)
        result = checkUserCred(valid_login_form)
        assert result is True
        assert current_user.is_authenticated
        assert current_user.name == data.name
        assert current_user.email == data.email