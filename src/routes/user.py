from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from src.utils.auth import *
from src.models.user_schema import *
from src.utils.dbs import *

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/register', methods=['OPTIONS', 'POST'])
def register():
    if request.method == 'OPTIONS':
        return jsonify({"message": "Preflight request"}), 200

    try:
        data = user_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    if get_user_by_username(data['username']) is not None:
        return jsonify({'message': 'Username already exists.'}), 400

    user_data = {
        'username': data['username'],
        'fullname': data['fullname'],
        'password': hash_password(data['password']),
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    }
    try:
        add_new_users(user_data)
    except Exception as e:
        return jsonify({'message': 'An error occurred while registering the user.', 'error': str(e)}), 500

    return jsonify({'message': 'User registered successfully!'}), 201


@user_bp.route('/login', methods=['OPTIONS', 'POST'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({"message": "Preflight request"}), 200

    try:
        data = request.get_json()
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    user = get_user_by_username(data['username'])
    if user is None:
        return jsonify({'message': 'Invalid username or password.'}), 401

    if not is_valid_password(user['password'], data['password']):
        return jsonify({'message': 'Invalid username or password.'}), 401
        # Set the expiration time to 30 minutes
    expires = timedelta(minutes=30)
    access_token = create_access_token(identity=user['username'], expires_delta=expires)
    refresh_token = create_refresh_token(identity=user['username'])

    return jsonify({'access_token': access_token,
                    'refresh_token': refresh_token,
                    'fullname': str(user['fullname'])
                    }), 200


@user_bp.route('/refresh', methods=['OPTIONS'])
def refresh_options():
    return jsonify({"message": "Preflight request"}), 200


@user_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200
