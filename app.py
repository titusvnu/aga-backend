from json import load
from flask import Flask
from dotenv import load_dotenv, dotenv_values
from extensions import db, migrate  # 👈 NEW
import os
from models import Merchandise      # ✅ Now safe here, no circular import

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    print("🔗 Connected to:", app.config['SQLALCHEMY_DATABASE_URI'])

    print(dotenv_values(".env"))
    db.init_app(app)
    migrate.init_app(app, db)

    from routes import register_routes
    register_routes(app, db)

    return app