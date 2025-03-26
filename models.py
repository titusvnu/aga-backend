from extensions import db

class Merchandise(db.Model):
    __tablename__ = 'merchandise'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable = False)
    category = db.Column(db.String(255), nullable = False)
    price = db.Column(db.Float, nullable = False)
    description = db.Column(db.String(255), nullable = False)

    def __repr__(self):
        return f'<{self.name}, is a {self.category}>'
    