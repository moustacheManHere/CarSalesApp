from application import login_manager, db
from application.models import User
from flask_login import login_user
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def checkUserCred(login):
    user = User.query.filter_by(email=login.email.data).first()
    if user:
        if bcrypt.check_password_hash(user.password, login.password.data):
            login_user(user)
            return True
    return False


def add_user(signup):
    password = bcrypt.generate_password_hash(signup.password.data)
    new_user = User(name=signup.name.data, email=signup.email.data, password=password)
    db.session.add(new_user)
    db.session.commit()
    return new_user.id


def updateProfile(user_id, form):
    try:
        user = User.query.get(user_id)

        if form.name.data is not None:
            user.name = form.name.data

        if form.new_password.data != "":
            new_password = bcrypt.generate_password_hash(form.new_password.data)
            user.password = new_password

        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False
