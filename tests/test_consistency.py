from application.models import *
from application.database import *
from application.ml import *
from application.auth import *
from application.forms import * 
import pytest 

@pytest.mark.parametrize("dataList", [
    [{'year': 5, 'transmission': 'Manual', 'mileage': 50000, 'fuelType': 'Petrol', 'tax': 'yes', 'mpg': 30.5, 'engineSize': 2.0, 'brand': 'audi'},
 {'year': 5, 'transmission': 'Manual', 'mileage': 50000, 'fuelType': 'Petrol', 'tax': 'yes', 'mpg': 30.5, 'engineSize': 2.0, 'brand': 'audi'},
 {'year': 5, 'transmission': 'Manual', 'mileage': 50000, 'fuelType': 'Petrol', 'tax': 'yes', 'mpg': 30.5, 'engineSize': 2.0, 'brand': 'audi'},],
 [{'year': 6, 'transmission': 'Manual', 'mileage': 50000, 'fuelType': 'Petrol', 'tax': 'yes', 'mpg': 30.5, 'engineSize': 2.0, 'brand': 'audi'},
 {'year': 6, 'transmission': 'Manual', 'mileage': 50000, 'fuelType': 'Petrol', 'tax': 'yes', 'mpg': 30.5, 'engineSize': 2.0, 'brand': 'audi'},
 {'year': 6, 'transmission': 'Manual', 'mileage': 50000, 'fuelType': 'Petrol', 'tax': 'yes', 'mpg': 30.5, 'engineSize': 2.0, 'brand': 'audi'},]
])
def test_regression_recommendation(app,dataList):
    with app.test_request_context("/"):
        first = True
        prev = None
        prevRec = None
        for data in dataList:
            model = RegressionModel()
            assert model is not None
            valid_form = NewRegressionForm(**data)
            assert valid_form is not None
            prediction = model.predict(valid_form)
            assert prediction is not None
            assert isinstance(prediction, float)
            recommended = list(get_recommended(valid_form,prediction))
            if not first:
                assert recommended == prevRec
                assert prediction == prev
            prev = prediction
            prevRec = recommended
            first = False

@pytest.mark.parametrize("searchParams", [
    [{'searchText': 'A', 'brand': 'Audi', 'fuelType': 'Petrol', 'tax': 'yes', 'minNumericInput': 10, 'maxNumericInput': 1000},
    {'searchText': 'A', 'brand': 'Audi', 'fuelType': 'Petrol', 'tax': 'yes', 'minNumericInput': 10, 'maxNumericInput': 1000},
    {'searchText': 'A', 'brand': 'Audi', 'fuelType': 'Petrol', 'tax': 'yes', 'minNumericInput': 10, 'maxNumericInput': 1000}],
    [{'searchText': 'A', 'brand': 'Audi', 'fuelType': 'Petrol', 'tax': 'no', 'minNumericInput': 100, 'maxNumericInput': 1200},
    {'searchText': 'A', 'brand': 'Audi', 'fuelType': 'Petrol', 'tax': 'no', 'minNumericInput': 100, 'maxNumericInput': 1200},
    {'searchText': 'A', 'brand': 'Audi', 'fuelType': 'Petrol', 'tax': 'no', 'minNumericInput': 100, 'maxNumericInput': 1200}]
])

def test_search_results(app,searchParams):
    with app.test_request_context("/"):
        first = True
        prev = None
        for data in searchParams:
            valid_form = CarSearchForm(**data)
            assert valid_form is not None
            results = list(filter_cars(valid_form))
            if not first:
                assert results == prev
            prev = results
            first = False

