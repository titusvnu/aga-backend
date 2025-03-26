from app import create_app
from os import environ
from dotenv import load_dotenv

load_dotenv()
flask_app = create_app()



if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=environ.get('SERVER_PORT'), debug=True)