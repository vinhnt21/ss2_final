from flask import Flask
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from src.routes.chat import chat_bp
from src.routes.user import user_bp

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
jwt = JWTManager(app)

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(chat_bp, url_prefix='/chat')


@app.route('/', methods=['POST'])
def home():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)
