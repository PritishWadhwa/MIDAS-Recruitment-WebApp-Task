from flask import Flask, render_template, url_for, redirect, session
from authlib.integrations.flask_client import OAuth


app = Flask(__name__)
app.secret_key = 'random secret'

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id="966548218605-9sk353h754pe97u9i8l1md3svc12kuqr.apps.googleusercontent.com",
    client_secret="m4LyDJk6y0okXix0YVXHQetL",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    # This is only needed if using openId to fetch user info
    # userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
)


@app.route('/')
def mainPage():
    return render_template('index.html')


@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    # resp.raise_for_status()
    user_info = resp.json()
    # do something with the token and profile
    return redirect('/')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


if __name__ == '__main__':
    app.static_folder = 'static'
    app.debug = True
    app.run()
