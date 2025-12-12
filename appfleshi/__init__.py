# appfleshi/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask_session import Session
import os
import json

load_dotenv()

app = Flask(__name__)

# Configurações de Sessão e Segurança
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = False  # Correção para MismatchingStateError (Cookie)
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Correção para MismatchingStateError (Cookie)
app.config['SESSION_COOKIE_SECURE'] = True  # Correção para MismatchingStateError (Cookie)
app.config['SECRET_KEY'] = 'uma_chave_secreta_muito_longa_e_aleatoria_para_fleshi_1234567890'

app.config['SESSION_SERIALIZER'] = json

# Configurações de Aplicação e Variáveis de Ambiente ---
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///datafleshi.db"
app.config['UPLOAD_FOLDER'] = 'static/posts_photos'

app.config['AUTH0_DOMAIN'] = os.getenv('AUTH0_DOMAIN')
app.config['AUTH0_CLIENT_ID'] = os.getenv('AUTH0_CLIENT_ID')
app.config['AUTH0_CLIENT_SECRET'] = os.getenv('AUTH0_CLIENT_SECRET')
app.config['AUTH0_CALLBACK_URL'] = os.getenv('AUTH0_CALLBACK_URL')
app.config['AUTH0_LOGOUT_URL'] = os.getenv('AUTH0_LOGOUT_URL')


# Inicializa o Flask-Session (Ordem Correta)
sess = Session(app)

# Inicializa extensões de DB e Segurança
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'homepage'

# Inicializa Authlib/OAuth
oauth = OAuth(app)

# Obtendo JWKS_URI
AUTH0_METADATA_URL = f'https://{app.config["AUTH0_DOMAIN"]}/.well-known/openid-configuration'

auth0 = oauth.register(
    'auth0',
    server_metadata_url=AUTH0_METADATA_URL,

    client_id=app.config['AUTH0_CLIENT_ID'],
    client_secret=app.config['AUTH0_CLIENT_SECRET'],

    api_base_url=f'https://{app.config["AUTH0_DOMAIN"]}/',

    client_kwargs={'scope': 'openid profile email'},
)

from appfleshi import routes