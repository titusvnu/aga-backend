from extensions import db
from datetime import datetime
class Merchandise(db.Model):
    __tablename__ = 'merchandise'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable = False)
    category = db.Column(db.String(255), nullable = False)
    price = db.Column(db.Float, nullable = False)
    description = db.Column(db.String(255), nullable = False)
    images = db.relationship('Image', backref='merchandise', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<{self.name}, is a {self.category}>'
    
    
class Image(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(512), nullable=False)
    purpose = db.Column(db.String(50), nullable=False, default="merchandise")
    merchandise_id = db.Column(db.Integer, db.ForeignKey('merchandise.id'), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Image {self.url} ({self.purpose})>'
