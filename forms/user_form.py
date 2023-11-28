from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField, EmailField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    first_name = StringField("Name", validators=[DataRequired()], render_kw={"placeholder": "first name"})
    last_name = StringField("Surname", validators=[DataRequired()], render_kw={"placeholder": "last name"})
    email = EmailField("Email ID", validators=[DataRequired()], render_kw={"placeholder": "enter email id"})
    bio = TextAreaField("Biography", render_kw={"placeholder": "additional details"})
    address = StringField("Address Line 1",
                          render_kw={"placeholder": "enter address line 1"})
    address2 = StringField("Address Line 2",
                           render_kw={"placeholder": "enter address line 2"})
    city = StringField("City", render_kw={"placeholder": "enter city"})
    state = StringField("State", render_kw={"placeholder": "enter state"})
    zip = StringField("Zip Code", render_kw={"placeholder": "postal code"})
    country = StringField("Country", render_kw={"placeholder": "country"})
    phone = StringField("Mobile Number", render_kw={"placeholder": "enter phone number"})
    current_password = PasswordField("Your current password",
                                     render_kw={"placeholder": "current password"})
    password = PasswordField("Enter new password",
                             render_kw={"placeholder": "new password"})
    confirm_password = PasswordField("Repeat your new password",
                                     render_kw={"placeholder": "confirm new password"})
    email_marketing_opt_in = BooleanField('Opt in to email marketing')
    text_marketing_opt_it = BooleanField('Opt in to text marketing')
    submit = SubmitField("Save Profile")

