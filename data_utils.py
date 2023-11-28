from settings import db, app
from db_models import Users
from flask import session
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError


def add_user(first_name, last_name, email, password):
    hashed_password = generate_password_hash(password,
                                             method="pbkdf2:sha256:600000",
                                             salt_length=8)

    new_user = Users()
    new_user.first_name = first_name
    new_user.last_name = last_name
    new_user.email = email
    new_user.password = hashed_password

    try:
        db.session.add(new_user)
        db.session.commit()
        app.logger.info(f"{email} created successfully {session['ctx']}")
        return new_user
    except SQLAlchemyError as e:
        print(f'Error while writing record: {e}')
        app.logger.error(f'REGISTER USER ERROR {email}: {e} {session["ctx"]}')
        return False


def authenticate_user(email, password):
    try:
        user = db.session.query(Users).filter_by(email=email).first()
        if user:
            hashed_password = user.password
            if check_password_hash(hashed_password, password):
                return user
            else:
                app.logger.critical(f'INVALID PASSWORD {email} {session["ctx"]}')
                return False
        else:
            app.logger.warning(f'USER DOES NOT EXIST {email} {session["ctx"]}')
            return False
    except SQLAlchemyError as e:
        print(f'Error while searching for user ({email}): {e}')
        app.logger.error(f'AUTHENTICATION ERROR ({email}): {e}  {session["ctx"]}')
        return False


def update_dashboard(first_name, last_name, email, phone, address, address2, city, state, zip, country, bio,
                     email_marketing, text_marketing):
    user = db.session.query(Users).filter_by(id=current_user.id).first()
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.phone = phone
    user.address = address
    user.address2 = address2
    user.city = city
    user.state = state
    user.zip = zip
    user.country = country
    user.bio = bio
    user.email_marketing_opt_in = email_marketing
    user.text_message_marketing_opt_in = text_marketing
    try:
        db.session.add(user)
        db.session.commit()
        app.logger.info(f"User #{user.id} profile updated successfully {session['ctx']}")
        return True
    except SQLAlchemyError as e:
        print(f'Error while writing record: {e}')
        app.logger.error(f'DASHBOARD UPDATE ERROR {e} {session["ctx"]}')
        return False

