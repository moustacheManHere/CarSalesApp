import pytest
from application.models import *
from application.database import *
from application.forms import *
from application.ml import *
from application.forms import * 

@pytest.mark.parametrize("invalid_params, error_message", [
    ({'name': 'Test User', 'email': 'test@example.com'}, "Missing password"),
    ({'name': 'Test User', 'password': 'password'}, "Missing email"),
    ({'email': 'test@example.com', 'password': 'password'}, "Missing name"),
    ({}, "Missing name, email, and password")
])
@pytest.mark.xfail(strict=True)
def test_user_init_invalid_params(invalid_params, error_message,capsys):
    with capsys.disabled():
        test_user = User(**invalid_params)
        print(error_message)
        assert test_user is not None

@pytest.mark.parametrize("invalid_data", [
    {'year': -5, 'transmission': 'Manual', 'mileage': 50000, 'fuelType': 'Petrol', 'tax': 200, 'mpg': 30.5, 'engineSize': 2.0, 'brand': 'Toyota'},
    {'year': 50, 'transmission': 'Automatic', 'mileage': -1000, 'fuelType': 'Petrol', 'tax': 200, 'mpg': 30.5, 'engineSize': 2.0, 'brand': 'Toyota'},
    {'year': 10, 'transmission': 'Manual', 'mileage': 50000, 'fuelType': 'InvalidFuelType', 'tax': 200, 'mpg': 30.5, 'engineSize': 2.0, 'brand': 'Toyota'},
])
@pytest.mark.xfail(strict=True)
def test_new_regression_form_validation(app,invalid_data):
    with app.test_request_context("/"):
        form = NewRegressionForm(**invalid_data)
        assert form.validate()

@pytest.mark.parametrize("invalid_data", [
    {'searchText': 'Car123', 'brand': 'InvalidBrand', 'fuelType': 'Petrol', 'tax': 'yes', 'minNumericInput': -10, 'maxNumericInput': 1000},
    {'searchText': 'Car123', 'brand': 'Toyota', 'fuelType': 'InvalidFuelType', 'tax': 'yes', 'minNumericInput': 100, 'maxNumericInput': 'invalid'},
])
@pytest.mark.xfail(strict=True)
def test_car_search_form_validation(app,invalid_data):
    with app.test_request_context("/"):
        form = CarSearchForm(**invalid_data)
        assert form.validate()

@pytest.mark.parametrize("invalid_data", [
    {'email': 'invalid_email', 'password': 'short'},
    {'email': 'valid_email@example.com', 'password': ''},
])
@pytest.mark.xfail(strict=True)
def test_login_form_validation(app,invalid_data):
    with app.test_request_context("/"):
        form = LoginForm(**invalid_data)
        assert form.validate()

@pytest.mark.parametrize("invalid_data", [
    {'name': '', 'email': 'invalid_email', 'password': 'short', 'confirm_password': 'not_matching'},
    {'name': 'Valid Name', 'email': 'valid_email@example.com', 'password': '', 'confirm_password': 'matching'},
    
])
@pytest.mark.xfail(strict=True)
def test_signup_form_validation(app,invalid_data):
    with app.test_request_context("/"):
        form = SignupForm(**invalid_data)
        assert form.validate()

@pytest.mark.parametrize("invalid_data", [
   {'name': '', 'new_password': 'short'}
])
@pytest.mark.xfail(strict=True)
def test_update_profile_form_validation(app,invalid_data):
    with app.test_request_context("/"):

        form = UpdateProfileForm(**invalid_data)
        assert form.validate()

@pytest.mark.parametrize("invalid_data", [
   ({'year': 'invalid', 'transmission': 'Manual', 'mileage': 50000, 'fuelType': 'Petrol', 'tax': 200, 'mpg': 30.5, 'engineSize': 2.0, 'brand': 'audi'}, "Invalid year value"),
    ({'year': 5, 'transmission': 'InvalidTransmission', 'mileage': 50000, 'fuelType': 'Petrol', 'tax': 200, 'mpg': 30.5, 'engineSize': 2.0, 'brand': 'audi'}, "Invalid transmission value"),
    ({'year': 5, 'transmission': 'Manual', 'mileage': 'invalid', 'fuelType': 'Petrol', 'tax': 200, 'mpg': 30.5, 'engineSize': 2.0, 'brand': 'audi'}, "Invalid mileage value"),
    ({'year': 5, 'transmission': 'Manual', 'mileage': 50000, 'fuelType': 'InvalidFuelType', 'tax': 200, 'mpg': 30.5, 'engineSize': 2.0, 'brand': 'audi'}, "Invalid fuelType value"),
    ({'year': 5, 'transmission': 'Manual', 'mileage': 50000, 'fuelType': 'Petrol', 'tax': 'invalid', 'mpg': 30.5, 'engineSize': 2.0, 'brand': 'audi'}, "Invalid tax value"),
    
])
@pytest.mark.xfail(strict=True)
def test_regression_model_invalid(app,invalid_data):
    with app.test_request_context("/"):
        model = RegressionModel()
        assert model is not None
        valid_form = NewRegressionForm(**invalid_data )
        assert valid_form is not None
        prediction = model.predict(valid_form)
        assert prediction is not None
        assert isinstance(prediction, float)

invalid_methods = ["PUT", "DELETE", "PATCH"]
@pytest.mark.parametrize("method, path", [
    (method, "/") for method in invalid_methods
] + [
    (method, "/history") for method in invalid_methods
] + [
    (method, "/wishlist") for method in invalid_methods
] + [
    (method, "/showcase") for method in invalid_methods
] + [
    (method, "/predict") for method in invalid_methods
] + [
    (method, "/login") for method in invalid_methods
] + [
    (method, "/signup") for method in invalid_methods
] + [
    (method, "/profile") for method in invalid_methods
])
@pytest.mark.xfail(strict=True)
def test_invalid_methods(client, method, path):
    response = client.open(path, method=method)
    assert response.status_code == 200