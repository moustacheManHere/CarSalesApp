from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    SelectField,
    SubmitField,
    FloatField,
    StringField,
    PasswordField,
)
from wtforms.validators import (
    InputRequired,
    NumberRange,
    Optional,
    DataRequired,
    Length,
    EqualTo,
)


car_brands = [
    ("audi", "Audi"),
    ("toyota", "Toyota"),
    ("skoda", "Skoda"),
    ("ford", "Ford"),
    ("vauxhall", "Vauxhall"),
    ("bmw", "BMW"),
    ("vw", "VW"),
    ("merc", "Mercedes"),
    ("hyundi", "Hyundi"),
]
fuelTypes = [("Petrol", "Petrol"), ("Diesel", "Diesel"), ("Hybrid", "Hybrid")]
transmissionTypes = [
    ("Manual", "Manual"),
    ("Semi-Auto", "Semi-Auto"),
    ("Automatic", "Automatic"),
]
yesNo = [("yes", "Yes"), ("no", "No")]


class NewRegressionForm(FlaskForm):
    year = IntegerField(
        "Car Age", validators=[InputRequired(), NumberRange(min=0, max=30)]
    )
    transmission = SelectField(
        "Type of Transmission", choices=transmissionTypes, validators=[InputRequired()]
    )
    mileage = IntegerField("Mileage", validators=[InputRequired(), NumberRange(min=1)])
    fuelType = SelectField(
        "Engine Fuel", choices=fuelTypes, validators=[InputRequired()]
    )
    tax = IntegerField("Road Tax (£)", validators=[InputRequired(), NumberRange(min=0)])
    mpg = FloatField("Miles Per Gallon", validators=[InputRequired(), NumberRange(min=1, max=100)])
    engineSize = FloatField("Engine Size in Litres", validators=[InputRequired(), NumberRange(min=0.1, max=30)])
    brand = SelectField("Car Brand", choices=car_brands, validators=[InputRequired()])
    submit = SubmitField("Predict")


class CarSearchForm(FlaskForm):
    searchText = StringField("Car Name", validators=[Optional()])
    brand = SelectField("Car Brand", choices=car_brands, validators=[Optional()])
    fuelType = SelectField(
        "Fuel Type",
        choices=[('any', 'Any'), ('petrol', 'Petrol'), ('diesel', 'Diesel'), ('hybrid', 'Hybrid')],
        validators=[Optional()],
    )
    tax = SelectField("Taxable?", choices=yesNo, validators=[Optional()])
    minNumericInput = IntegerField(
        "Min Value", validators=[Optional(), NumberRange(min=0)]
    )
    maxNumericInput = IntegerField(
        "Max Value", validators=[Optional(), NumberRange(min=1)]
    )
    submit = SubmitField("search")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Login")


class SignupForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")


class UpdateProfileForm(FlaskForm):
    name = StringField("Name", validators=[Optional()])
    new_password = PasswordField("New Password", validators=[Optional(), Length(min=6)])
    submit = SubmitField("Update Profile")
