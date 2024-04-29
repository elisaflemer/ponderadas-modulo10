from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, unset_jwt_cookies, get_jwt_identity
from .models import User, Task
from . import db

api_bp = Blueprint('api', __name__)


@api_bp.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, World!'})

@api_bp.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 409
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@api_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        response = jsonify({'login': True})
        set_access_cookies(response, access_token)
        return response
    return jsonify({'login': False}), 401

@api_bp.route('/logout', methods=['POST'])
def logout():
    response = jsonify({'logout': True})
    unset_jwt_cookies(response)
    return response

@api_bp.route('/tasks', methods=['GET', 'POST'])
@jwt_required()
def tasks():
    user_id = get_jwt_identity()
    if request.method == 'POST':
        title = request.json.get('title')
        task = Task(title=title, user_id=user_id)
        db.session.add(task)
        db.session.commit()
        return jsonify({'message': 'Task added successfully.'}), 201
    else:
        tasks = Task.query.filter_by(user_id=user_id).all()
        return jsonify({'tasks': [{'id': task.id, 'title': task.title, 'completed': task.completed} for task in tasks]})
    
@api_bp.route('/tasks/<int:id>', methods=['PUT', 'DELETE'])
@jwt_required()
def task(id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=id, user_id=user_id).first()
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    if request.method == 'PUT':
        task.completed = not task.completed
        db.session.commit()
        return jsonify({'message': 'Task updated successfully.'})
    else:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully.'})

@api_bp.route('/tasks/<int:id>/complete', methods=['PUT'])
@jwt_required()
def complete_task(id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=id, user_id=user_id).first()
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    task.completed = True
    db.session.commit()
    return jsonify({'message': 'Task completed successfully.'})

@api_bp.route('/tasks/<int:id>/incomplete', methods=['PUT'])
@jwt_required()
def incomplete_task(id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=id, user_id=user_id).first()
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    task.completed = False
    db.session.commit()
    return jsonify({'message': 'Task marked as incomplete successfully.'})


