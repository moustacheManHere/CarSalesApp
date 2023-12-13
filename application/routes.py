from flask import render_template, request, redirect, url_for
from flask_login import current_user
from application import app
from application.ml import RegressionModel
from application.forms import *
from application.auth import *
from application.database import *
from application.api import *


regressor = RegressionModel()


@app.route("/")
def index():
    return render_template("index.html", title="Giggles Gears")


@app.route("/history")
def history():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    history_data = getUserHist(current_user.get_id())
    return render_template("history.html", title="History", history_data=history_data)


@app.route("/wishlist")
def wishlist():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    wishlist = getUserWish(current_user.get_id())
    return render_template("wishlist.html", title="Wishlist", wishlist=wishlist)


@app.route("/showcase", methods=["GET", "POST"])
def showcase():
    carSearch = CarSearchForm()
    page = request.args.get("page", 1, type=int)
    cars = filter_cars(carSearch, page=page)
    return render_template(
        "showcase.html", title="Catalogue", form=carSearch, cars=cars
    )


@app.route("/predict", methods=["GET", "POST"])
def prediction():
    form = NewRegressionForm()
    if request.method == "GET":
        return render_template(
            "prediction.html", title="Prediction", form=form, predictedVal="Not yet"
        )
    if request.method == "POST":
        if form.validate_on_submit():
            predicted = regressor.predict(form)
            if current_user.is_authenticated:
                addHistory(form, current_user.get_id(), predicted)
            cars = get_recommended(form, predicted)
            return render_template(
                "prediction.html",
                title="prediction",
                form=form,
                predictedVal="{:,}".format(predicted),
                cars=cars,
            )
        else:
            return render_template(
                 "prediction.html", title="Prediction", form=form, predictedVal="Not yet"
            )
    else:
        return render_template(
            "prediction.html", title="Prediction", form=form, predictedVal="Not yet"
        )


@app.route("/login", methods=["GET", "POST"])
def login():
    login = LoginForm()
    if login.validate_on_submit():
        if checkUserCred(login):
            return redirect(url_for("index"))
        return render_template("login.html", title="Login", form=login)
    return render_template("login.html", title="Login", form=login)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    signup = SignupForm()
    if signup.validate_on_submit():
        add_user(signup)
        return redirect(url_for("index"))
    return render_template("signup.html", title="Signup", form=signup)


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    profForm = UpdateProfileForm()
    if profForm.validate_on_submit():
        updateProfile(current_user.get_id(), profForm)
        return redirect(url_for("profile"))
    return render_template("profile.html", title="Profile", form=profForm)
