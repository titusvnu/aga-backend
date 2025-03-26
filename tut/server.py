from flask import (Flask,
                    render_template, #Renders JS and HTML files
                      request, #Handles HTTP requests
                        jsonify, #Handle JSON formatted data in Python
                          make_response) # Handles HTTP Responses 

from flask_sqlalchemy import SQLAlchemy # An ORM library, manage database
from flask_cors import CORS 
from datetime import datetime
from os import environ #Read environment variables to connect database 


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') #Connect to database
CORS(app) #Enables CORS for all routes 

db = SQLAlchemy(app) 






class Userbase(db.Model):
    __tablename__= 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.entry_id


def json_format(self):
    return {'id': self.id, 'username': self.username, 'email': self.email}

with app.app_context():
    db.create_all()

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'It works!'}) #Return JSON data



@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = Userbase(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
        }), 201 #Return JSON data with status code 201
    except Exception as e:
        return make_response(jsonify({'Message:' : 'Error registering user',
                                       'error': str(e)}), 400) #Return JSON data with status code 400
    


@app.route('/api/flask/users', methods=['GET'])
def retrieve_users():
    try:
        users = Userbase.query.all()
        return jsonify([{'id': users.id, 'username': user.username, 'email': user.email} for user in users])
    except Exception as error:
        return make_response(jsonify({'Message:' : 'Error retrieving users',
                                       'error': str(error)}), 500) #Return JSON data with status code 500 (f)
     

@app.route('/api/flask/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = Userbase.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify({'username': user.username.json(), 'email': user.email.json()}), 200)
        else:
             return make_response(jsonify({'Message:' : 'User not Found'}), 404) 
    except Exception as error:
        return make_response(jsonify({'Message:' : 'Error getting User',
                                       'error': str(error)}), 404)

@app.route('/api/flask/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user = Userbase.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.username = data['username']
            user.email = data['email']
            db.session.commit()
            return make_response(jsonify({'Message:' : 'User updated'}), 200)
        else:
            return make_response(jsonify({'Message:' : 'User not Found'}), 404) 
    except Exception as error:
        return make_response(jsonify({'Message:' : 'Error updating User',
                                       'error': str(error)}), 404)
    

@app.route('api/flask/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = Userbase.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'Message:' : 'User deleted'}), 200)
        else:
            return make_response(jsonify({'Message:' : 'User not Found'}), 404) 
    except Exception as error:
        return make_response(jsonify({'Message:' : 'Error deleting User',
                                       'error': str(error)}), 404)



@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        
        return "POST!"
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080)
