from app import create_app, db
from sqlalchemy.sql import text
app = create_app()

with app.app_context():
    try:
        db.session.execute(text('SELECT 1'))
        print("✅ Connected to Supabase DB")
    except Exception as e:
        print("❌ Failed to connect:", e)