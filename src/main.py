from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, set_access_cookies
import requests as http_request
from database.database import db
from database.models import User, Task
import os
import sys

# Flask application initialization
app = Flask(__name__, template_folder="templates")
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/todo"
db.init_app(app)

# JWT configuration
app.config["JWT_SECRET_KEY"] = "goku-vs-vegeta"
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
jwt = JWTManager(app)

# Database setup command line argument
if len(sys.argv) > 1 and sys.argv[1] == 'create_db':
    with app.app_context():
        db.create_all()
    print("Database created successfully")
    sys.exit(0)

# Routes
@app.route("/api/v1")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/user-register", methods=["GET"])
def user_register():
    return render_template("register.html")

@app.route("/user-login", methods=["GET"])
def user_login():
    return render_template("login.html")

@app.route("/api/v1/login", methods=["POST"])
def login():
    print(request.json)
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        return render_template("error.html", message="Bad username or password"), 400
    token_data = http_request.post("http://localhost:5000/api/v1/token", json={"username": username, "password": password})
    if token_data.status_code != 200:
        return render_template("error.html", message="Bad username or password"), token_data.status_code
    response = jsonify({"success": True})
    set_access_cookies(response, token_data.json()['token'], max_age=60*60*24*7)
    return response

@app.route("/content", methods=["GET"])
@jwt_required()
def content():
    return render_template("content.html")

@app.route("/error", methods=["GET"])
def error():
    return render_template("error.html")

@app.route("/api/v1/users/<int:id>", methods=["GET"])
@jwt_required()
def get_user():
    user = User.query.get(get_jwt_identity())
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.serialize())

@app.route("/api/v1/users", methods=["GET"])
@jwt_required()
def get_users():
    current_user = User.query.get(get_jwt_identity())
    if current_user.name != "admin":
        return jsonify({"error": "Unauthorized"}), 401

    users = User.query.all()
    return jsonify([user.serialize() for user in users])

@app.route("/api/v1/users", methods=["POST"])
def create_user():
    data = request.json
    user = User(name=data["username"], email=data["email"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 201

@app.route("/api/v1/users/<int:id>", methods=["PUT"])
@jwt_required()
def update_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    data = request.json
    user.name = data["name"]
    user.email = data["email"]
    user.password = data["password"]
    db.session.commit()
    return jsonify(user.serialize())

@app.route("/api/v1/users/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"success": True}), 204

@app.route("/api/v1/token", methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(name=username, password=password).first()
    print(user)
    if user is None:
        return jsonify({"msg": "Bad username or password"}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify({"token": access_token, "user_id": user.id})

@app.route("/api/v1/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    tasks = Task.query.filter_by(user_id=get_jwt_identity()).all()
    return jsonify([task.serialize() for task in tasks])

@app.route("/api/v1/tasks/<int:id>", methods=["GET"])
@jwt_required()
def get_task(id):
    task = Task.query.filter_by(id=id, user_id=get_jwt_identity()).first()
    if task is None:
        return jsonify({"error": "Task not found or unauthorized access"}), 404
    return jsonify(task.serialize())

@app.route("/api/v1/tasks", methods=["POST"])
@jwt_required()
def create_task():
    data = request.json
    task = Task(title=data["title"], status=data["status"], user_id=get_jwt_identity())
    db.session.add(task)
    db.session.commit()
    return jsonify(task.serialize()), 201

@app.route("/api/v1/tasks/<int:id>", methods=["PUT"])
@jwt_required()
def update_task(id):
    task = Task.query.filter_by(id=id, user_id=get_jwt_identity()).first()
    if task is None:
        return jsonify({"error": "Task not found or unauthorized access"}), 404
    data = request.json
    task.title = data["title"]
    task.status = data["status"]
    db.session.commit()
    return jsonify(task.serialize())

@app.route("/api/v1/tasks/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_task(id):
    task = Task.query.filter_by(id=id, user_id=get_jwt_identity()).first()
    if task is None:
        return jsonify({"error": "Task not found or unauthorized access"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"success": 1}), 204

if __name__ == "__main__":
    app.run(debug=True)
