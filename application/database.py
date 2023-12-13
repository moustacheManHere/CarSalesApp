from application import db
from application.models import *
from application.ml import getRecommended


def add_entry(new_entry):
    try:
        db.session.add(new_entry)
        db.session.commit()
        return new_entry.id
    except Exception as error:
        print(error)
        db.session.rollback()
        return 0
    
def add_history(new_entry):
    try:
        db.session.add(new_entry)
        db.session.commit()
        return new_entry.histID
    except Exception as error:
        print(error)
        db.session.rollback()
        return 0

def remove_wishlist(car_id, user_id):
    try:
        entry = db.get_or_404(Wishlist, (user_id, car_id))
        db.session.delete(entry)
        db.session.commit()
    except Exception as error:
        print(error)
        db.session.rollback()
        return 0


def remove_entry(id, Entry):
    try:
        entry = db.get_or_404(Entry, id)
        db.session.delete(entry)
        db.session.commit()
    except Exception as error:
        print(error)
        db.session.rollback()
        return 0


def addHistory(form, id, predicted):
    hist = History(
        id,
        form.year.data,
        form.transmission.data,
        form.mileage.data,
        form.fuelType.data,
        form.tax.data,
        form.mpg.data,
        form.engineSize.data,
        form.brand.data,
        predicted,
    )
    add_entry(hist)


def addWishlist(car_id, current_id):
    wish = Wishlist(user_id=current_id, car_id=car_id)
    try:
        db.session.add(wish)
        db.session.commit()
        return 1
    except Exception as error:
        print(error)
        db.session.rollback()
        return 0


def filter_cars(form, page=1, per_page=9):
    try:
        query = Car.query.with_entities(
            Car.id, Car.model, Car.brand, Car.year, Car.mpg, Car.mileage, Car.price
        )
        if form.searchText.data:
            query = query.filter(Car.model.ilike(f"%{form.searchText.data}%"))
        if form.brand.data and form.brand.data != "any":
            query = query.filter_by(brand=form.brand.data)
        if form.fuelType.data and form.fuelType.data != "any":
            query = query.filter_by(fuelType=form.fuelType.data)
        if form.tax.data and form.tax.data == "yes":
            query = query.filter(Car.tax > 0)
        if form.minNumericInput.data is not None:
            query = query.filter(Car.price >= form.minNumericInput.data)
        if form.maxNumericInput.data is not None:
            query = query.filter(Car.price <= form.maxNumericInput.data)
        paginated_result = query.paginate(page=page, per_page=per_page, error_out=False)
        return paginated_result

    except Exception as error:
        print(error)
        return []


def get_recommended(form, predicted):
    try:
        query = Car.query.with_entities(
            Car.id,
            Car.model,
            Car.brand,
            Car.year,
            Car.mpg,
            Car.mileage,
            Car.price,
            Car.engineSize,
        )

        if form.brand.data:
            query = query.filter_by(brand=form.brand.data)

        if form.fuelType.data:
            query = query.filter_by(fuelType=form.fuelType.data)

        if form.transmission.data:
            query = query.filter_by(transmission=form.transmission.data)

        if form.tax.data and form.tax.data != "yes":
            query = query.filter(Car.tax == 0)

        if form.tax.data and form.tax.data == "yes":
            query = query.filter(Car.tax > 0)

        result = query.all()
        if len(result) == 0:
            return result
        result_dict_list = result
        num_data = {
            "id": [row[0] for row in result_dict_list],
            "year": [row[3] for row in result_dict_list],
            "price": [row[6] for row in result_dict_list],
            "mileage": [row[5] for row in result_dict_list],
            "mpg": [row[4] for row in result_dict_list],
            "engineSize": [row[7] for row in result_dict_list],
        }
        input_df = {
            "year": [form.year.data],
            "price": [predicted],
            "mileage": [form.mileage.data],
            "mpg": [form.mpg.data],
            "engineSize": [form.engineSize.data],
        }

        top3_rows = getRecommended(num_data, input_df)
        result = query.filter(Car.id.in_(top3_rows["id"].tolist())).all()
        return result

    except Exception as error:
        print(error)
        return []


def getUserHist(user_id):
    try:
        history_data = History.query.filter_by(id=user_id).all()
        return history_data
    except Exception as error:
        print(error)
        return []


def getUserWish(user_id):
    try:
        wishlist_data = (
            Wishlist.query.filter_by(user_id=user_id)
            .join(Car, Car.id == Wishlist.car_id)
            .add_columns(
                Car.id.label("car_id"),
                Car.model,
                Car.brand,
                Car.year,
                Car.mpg,
                Car.mileage,
                Car.price,
                Wishlist.date,
            )
            .all()
        )
        return wishlist_data
    except Exception as error:
        print(error)
        return []
