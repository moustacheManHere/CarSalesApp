from flask_login import current_user
import pytest
import json

@pytest.mark.parametrize(
    "test_input",
    [
        {
            "year": 7,
            "transmission": "Manual",
            "mileage": 50000,
            "fuelType": "Petrol",
            "tax": -200,
            "mpg": 30.5,
            "engineSize": 2.0,
            "brand": "Audi",
        },
        {
            "year": -1000,
            "transmission": "Automatic",
            "mileage": 10000,
            "fuelType": "Diesel",
            "tax": 500,
            "mpg": -10.5, 
            "engineSize": 5.0,
            "brand": "Audi",
        },
    ],
)
@pytest.mark.xfail(reason="XFail for handling extreme values")
def test_predict_price(app,client, test_input):
    with app.test_request_context("/"):
        response = client.post(
            "/api/predict",
            data=json.dumps(test_input),
            content_type="application/json",
        )
        assert response.status_code == 200
        body = json.loads(response.get_data(as_text=True))
        assert "predictedVal" in body