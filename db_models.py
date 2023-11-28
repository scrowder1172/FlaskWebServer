from settings import app, db
from sqlalchemy.sql import func
from flask_login import UserMixin


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    bio = db.Column(db.String)
    address = db.Column(db.String)
    address2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip = db.Column(db.String)
    country = db.Column(db.String)
    phone = db.Column(db.String)
    agree_to_terms = db.Column(db.Boolean, nullable=False, default=True)
    email_marketing_opt_in = db.Column(db.Boolean)
    text_message_marketing_opt_in = db.Column(db.Boolean)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created_ts = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<ID "{self.id}">'


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

