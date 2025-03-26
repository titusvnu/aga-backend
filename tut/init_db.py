from flask import Flask
from extensions import db
from models import Merchandise
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
print(os.environ.get('DATABASE_URL'))# == 'postgresql://postgres:zlxGKBkIvFYFCirg@db.enawxdfvxerqwripzzsa.supabase.co:5432/postgres') 
db.init_app(app)

with app.app_context():
    db.create_all()
    print("✅ Tables created successfully in Supabase")