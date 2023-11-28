from flask import render_template, request, redirect, url_for, flash, abort, session
from flask_login import login_user, login_required, current_user, logout_user
from settings import app, db, login_manager#, gravatar
from db_models import Users
from urllib.parse import urlparse, urljoin
from data_utils import add_user, authenticate_user, update_dashboard
from forms.all_forms import RegistrationForm, UserForm, LoginForm
import uuid


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route('/')
def go_home():
    session['ctx'] = {"request_id": str(uuid.uuid4()),
                      "ip": request.remote_addr,
                      "remote_user": request.remote_user}
    app.logger.info(f'A user visited the home page {session["ctx"]}')
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def registration_route():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        first_name = registration_form.first_name.data
        last_name = registration_form.last_name.data
        email = registration_form.email.data
        password = registration_form.password.data
        confirm_password = registration_form.confirm_password.data
        agree_to_terms = request.form.get('terms_opt')

        print(f'Registration Data:\n'
              f'First Name: {first_name}\n'
              f'Last Name: {last_name}\n'
              f'Email: {email}\n'
              f'Password: {password}\n'
              f'Confirm Password: {confirm_password}\n'
              f'Terms: {agree_to_terms}')

        if not agree_to_terms:
            flash('Please agree to terms before continuing', 'danger')
            return redirect(url_for('registration_route'))

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('registration_route'))

        if Users.query.filter_by(email=email).first():
            flash("You've already signed up with that email, log in instead!", 'info')
            app.logger.warning(f'{email} already exists')
            return redirect(url_for('login'))

        user = add_user(first_name=first_name, last_name=last_name, email=email, password=password)
        if user:
            login_user(user)
            return redirect(url_for('user_dashboard_route'))
        else:
            flash('Registration failed. Please try again.', 'danger')
            return redirect(url_for('registration_route'))

    return render_template('register.html', form=registration_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST':
        next_url = request.args.get('next')
        user = authenticate_user(login_form.email.data, login_form.password.data)
        if user:
            login_user(user)
            if (next_url and is_safe_url(next_url)) or not next_url:
                return redirect(next_url or url_for('user_dashboard_route'))
            else:
                app.logger.error(f'Next URL ({next_url}) not safe. Aborting... {session["ctx"]}')
                abort(400)
            return redirect(url_for('user_dashboard_route'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=login_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('go_home'))


@app.route('/user_dashboard', methods=['GET', 'POST'])
@login_required
def user_dashboard_route():
    user = db.session.query(Users).filter_by(id=current_user.id).first()
    user_form = UserForm()
    if user_form.validate_on_submit():
        if update_dashboard(first_name=user_form.first_name.data,
                            last_name=user_form.last_name.data,
                            email=user_form.email.data,
                            phone=user_form.phone.data,
                            address=user_form.address.data,
                            address2=user_form.address2.data,
                            city=user_form.city.data,
                            state=user_form.state.data,
                            zip=user_form.zip.data,
                            country=user_form.country.data,
                            bio=user_form.bio.data,
                            email_marketing=user_form.email_marketing_opt_in.data,
                            text_marketing=user_form.text_marketing_opt_it.data):
            flash('Profile updated successfully', 'success')
        else:
            flash('Profile update failed. Please try again.', 'danger')
        return redirect(url_for('user_dashboard_route'))
    elif user:
        user_form.first_name.data = user.first_name
        user_form.last_name.data = user.last_name
        user_form.email.data = user.email
        user_form.phone.data = user.phone
        user_form.address.data = user.address
        user_form.address2.data = user.address2
        user_form.city.data = user.city
        user_form.state.data = user.state
        user_form.zip.data = user.zip
        user_form.country.data = user.country
        user_form.bio.data = user.bio
        if user.email_marketing_opt_in:
            user_form.email_marketing_opt_in.data = user.email_marketing_opt_in
        if user.text_message_marketing_opt_in:
            user_form.text_marketing_opt_it.data = user.text_message_marketing_opt_in
    return render_template('user_dashboard.html', form=user_form)


@app.route('/terms_of_service')
def terms_of_service_route():
    return render_template('terms_of_service.html')


@app.route('/privacy_policy')
def privacy_policy_route():
    return render_template('privacy_policy.html')


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


if __name__ == "__main__":
    app.run(debug=True, port=5008)
