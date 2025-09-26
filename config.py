from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import os
from flask_login import LoginManager
from sqlalchemy import MetaData
from dotenv import load_dotenv
from supabase import create_client, Client
from flask_admin import Admin
from flask_talisman import Talisman

load_dotenv(".env.database")
load_dotenv(".env.app")

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase_client: Client = create_client(supabase_url, supabase_key)

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = 'arquivos'
app.config['ALLOWED_EXTENSIONS'] = ['.pdf', '.png', '.jpg', '.jpeg']
app.secret_key = os.getenv("SECRET_KEY")

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,   # Evita acesso via JavaScript
    SESSION_COOKIE_SECURE=True,     # Apenas HTTPS
    SESSION_COOKIE_SAMESITE='Lax'   # Evita envio cruzado
)

login_manager = LoginManager(app)
login_manager.login_view = 'login_bp.login'
login_manager.login_message = "Você precisa estar logado para acessar esta página"
login_manager.login_message_category = "error"



CORS(app)

csp = {
    'default-src': [
        '\'self\'',
        'ka-f.fontawesome.com'
    ],
    'script-src': [
        '\'self\'',
        'https://kit.fontawesome.com',
    ],
    'style-src': [
        '\'self\'',
        'https://kit.fontawesome.com'
    ],
    'font-src': [
        '\'self\'',
        'https://kit.fontawesome.com'
    ]
}

nonce = [
    'default-src',
    'script-src',
    'style-src',
    'font-src'
]

Talisman(app, content_security_policy=csp, content_security_policy_nonce_in=nonce)

db = SQLAlchemy(app, metadata=MetaData(naming_convention=naming_convention))

with app.app_context():
    # db.drop_all()
    db.create_all()
        
migrate = Migrate(app, db, render_as_batch=True)

admin = Admin(app, name="Painel de Controle do Admin", template_mode='bootstrap3')
