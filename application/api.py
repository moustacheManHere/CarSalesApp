from flask import jsonify, request, redirect, url_for
from flask_login import login_required, logout_user, current_user
from application import app
from application.ml import RegressionModel
from application.forms import *
from application.auth import *
from application.database import *


regressor = RegressionModel()


@app.route("/api/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/api/predict", methods=["POST"])
def predictPrice():
    data = request.get_json()
    year = data.get("year")
    transmission = data.get("transmission")
    mileage = data.get("mileage")
    fuelType = data.get("fuelType")
    tax = data.get("tax")
    mpg = data.get("mpg")
    engineSize = data.get("engineSize")
    brand = data.get("brand")
    form = NewRegressionForm(
        year=year,
        transmission=transmission,
        mileage=mileage,
        fuelType=fuelType,
        tax=tax,
        mpg=mpg,
        engineSize=engineSize,
        brand=brand,
    )
    try:
        predicted = regressor.predict(form)
        return jsonify({"predictedVal": predicted}), 200
    except:
        errors = {field: form.errors[field][0] for field in form.errors}
        print(errors)
        return jsonify({"error": "Validation failed", "errors": errors}), 403



@app.route("/api/add_history", methods=["POST"])
def api_add_history():
    try:
        data = request.get_json()
        form_data = data.get("form")
        id_value = data.get("id")
        predicted_value = data.get("predicted")
        addHistory(form_data, id_value, predicted_value)
        return jsonify({"success": True, "message": "History added successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/api/check_user_cred", methods=["POST"])
def api_check_user_cred():
    try:
        data = request.get_json()
        login = LoginForm(email=data.get("email"), password=data.get("password"))
        success = checkUserCred(login)

        if success:
            return jsonify({"success": True, "message": "User credentials are valid"}),200
        else:
            return jsonify({"success": False, "message": "Invalid user credentials"}),401
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}),400


@app.route("/api/add_user", methods=["POST"])
def api_add_user():
    try:
        data = request.get_json()
        signup = SignupForm(
            name=data.get("name"),
            email=data.get("email"),
            password=data.get("password"),
        )
        id = add_user(signup)

        return jsonify({"success": True, "id": id}),200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e)}),400

@app.route("/api/remove_user/<int:id>", methods=["POST"])
def api_remove_user(id):
    try:
        remove_entry(id,User)

        return jsonify({"success": True, "id": id}),200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e)}),400

@app.route("/api/update", methods=["POST"])
def api_update_profile():
    data = request.get_json()
    form = UpdateProfileForm(data=data)

    if form.validate():
        user_id = data.get("user_id")
        if user_id is not None:
            success = updateProfile(user_id, form)
            return jsonify({"success": success, "id": user_id}), 200
    return jsonify({"error": "Invalid form data", "errors": form.errors}), 400


@app.route("/api/add_to_wishlist/<int:car_id>", methods=["POST"])
def add_to_wishlist_route(car_id):
    if current_user.is_authenticated:
        addWishlist(current_id=current_user.get_id(), car_id=car_id)
        return redirect(url_for("showcase"))
    return redirect(url_for("login"))


@app.route("/api/add_to_wishlist_pred/<int:car_id>", methods=["POST"])
def add_to_wishlist_pred_route(car_id):
    if current_user.is_authenticated:
        addWishlist(current_id=current_user.get_id(), car_id=car_id)
        return redirect(url_for("prediction"))
    return redirect(url_for("login"))


@app.route("/api/remove_hist/<int:hist>", methods=["POST"])
def removeHistory(hist):
    if current_user.is_authenticated:
        remove_entry(hist, History)
        return redirect(url_for("history"))
    return redirect(url_for("login"))


@app.route("/api/remove_wish/<int:wish>", methods=["POST"])
def removeWish(wish):
    if current_user.is_authenticated:
        remove_wishlist(wish, current_user.get_id())
        return redirect(url_for("wishlist"))
    return redirect(url_for("login"))
