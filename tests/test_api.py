from flask_login import current_user
import pytest
import json

def test_add_user(client):
    data = {"name":"Spooky Do","email":"lol5@gmail.com","password":"ligmaballs"}
    response = client.post("/api/add_user",
                           data=json.dumps(data),
                            content_type="application/json")
    assert response.status_code ==200
    body = json.loads(response.get_data(as_text=True))
    assert body["id"]
    response = client.post(f'/api/remove_user/{body["id"]}')
    assert response.status_code == 200

def test_login_logout(app,client):
    with app.test_request_context("/"):
        data = {"name":"Spooky Do","email":"lol5@gmail.com","password":"ligmaballs"}
        response = client.post("/api/add_user",
                            data=json.dumps(data),
                                content_type="application/json")
        assert response.status_code ==200
        body = json.loads(response.get_data(as_text=True))
        assert body["id"]

        response2 = client.post("/api/check_user_cred",
                            data=json.dumps(data),
                                content_type="application/json")
        assert response2.status_code ==200
        assert current_user.id == body["id"]

        response = client.post(f'/api/remove_user/{body["id"]}')
        assert response.status_code == 200

def test_predict_price(app,client):
    with app.test_request_context("/"):
        data = {
            "year": 7,
            "transmission": "Manual",
            "mileage": 50000,
            "fuelType": "Petrol",
            "tax": 200,
            "mpg": 30.5,
            "engineSize": 2.0,
            "brand": "audi",
        }
        response = client.post("/api/predict", data=json.dumps(data), 
                               content_type="application/json")
        assert response.status_code == 200
        body = json.loads(response.get_data(as_text=True))
        assert "predictedVal" in body

