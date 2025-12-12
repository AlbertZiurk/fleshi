from flask import render_template, url_for, redirect, session, request
from flask_login import login_required, login_user, logout_user, current_user
from appfleshi import app, database, bcrypt, auth0
from appfleshi.forms import LoginForm, RegisterForm, PhotoForm
from appfleshi.models import User, Photo
import os
from werkzeug.utils import secure_filename

@app.route('/', methods=['GET', 'POST'])
def homepage():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user)
            if 'auth0_user' in session:
                session.pop('auth0_user')

            return redirect(url_for('feed'))
    return render_template('homepage.html', form=login_form)

@app.route('/login/auth0')
def login_auth0():
    return auth0.authorize_redirect(redirect_uri=app.config['AUTH0_CALLBACK_URL'], prompt='login')


@app.route('/callback') # JAMAIS TOQUE NISSO
def callback():
    if request.args.get('error') == 'access_denied':
        return redirect(url_for('homepage'))

    try:
        token = auth0.authorize_access_token()
    except Exception as e:
        print(f"Erro de autorização do Auth0: {type(e).__name__}: {e}")
        return redirect(url_for('homepage'))

    user_info = auth0.get('userinfo').json()

    user = User.query.filter_by(email=user_info['email']).first()

    if not user:

        base_username = user_info['name'].replace(' ', '').lower()
        username = base_username
        counter = 1

        while User.query.filter_by(username=username).first():
            username = f"{base_username}{counter}"
            counter += 1

        password_dummy = bcrypt.generate_password_hash("AUTH0_NO_PASSWORD_SET")

        try:
            user = User(username=username, email=user_info['email'], password=password_dummy)
            database.session.add(user)
            database.session.commit()
            login_user(user)
            session['auth0_user'] = True
            return redirect(url_for('feed'))

        except Exception as e:

            print(f"Erro ao salvar novo usuário Auth0: {e}")
            database.session.rollback()
            return redirect(url_for('homepage'))

    login_user(user)
    session['auth0_user'] = True

    return redirect(url_for('feed'))

@app.route("/createaccount", methods=['GET', 'POST'])
def createaccount():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        password = bcrypt.generate_password_hash(register_form.password.data)
        user = User(username=register_form.username.data, email=register_form.email.data, password=password)
        database.session.add(user)
        database.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('profile', user_id=user.id))
    return render_template('createaccount.html', form=register_form)

@app.route("/profile/<user_id>", methods=['GET', 'POST'])
@login_required
def profile(user_id):
    if int(user_id) == int(current_user.id):
        photo_form = PhotoForm()
        if photo_form.validate_on_submit():
            file = photo_form.photo.data
            secure_name = secure_filename(file.filename)
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], secure_name)
            file.save(path)
            photo = Photo(file_name=secure_name, user_id=current_user.id)
            database.session.add(photo)
            database.session.commit()
        return render_template('profile.html', user=current_user, form=photo_form)
    else:
        user = User.query.get(int(user_id))
        return render_template('profile.html', user=user, form=None)

@app.route("/logout")
@login_required
def logout():
    is_auth0_user = session.pop('auth0_user', False)
    logout_user()
   # return redirect(url_for('homepage'))

    if is_auth0_user:
        auth0_logout_url = f'https://{app.config["AUTH0_DOMAIN"]}/v2/logout?client_id={app.config["AUTH0_CLIENT_ID"]}&returnTo={url_for("homepage", _external=True)}'
        return redirect(auth0_logout_url)
    else:
        return redirect(url_for('homepage'))


@app.route("/feed")
@login_required
def feed():
    photos = Photo.query.order_by(Photo.upload_date.desc()).all()
    return render_template("feed.html", photos=photos)