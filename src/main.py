from flask import Flask, render_template, make_response
from database.database import db
from flask import jsonify, request
from database.models import User, Task
import requests as http_request
import os
from flask_jwt_extended import JWTManager, set_access_cookies


app = Flask(__name__, template_folder="templates")
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/todo"
db.init_app(app)
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "goku-vs-vegeta" 
# Seta o local onde o token será armazenado
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False 
jwt = JWTManager(app)
import sys
if len(sys.argv) > 1 and sys.argv[1] == 'create_db':
    # cria o banco de dados
    with app.app_context():
        db.create_all()
    # Finaliza a execução do programa
    print("Database created successfully")
    sys.exit(0)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/user-register", methods=["GET"])
def user_register():
    return render_template("register.html")

@app.route("/user-login", methods=["GET"])
def user_login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    # Verifica os dados enviados não estão nulos
    if username is None or password is None:
        # the user was not found on the database
        return render_template("error.html", message="Bad username or password")
    # faz uma chamada para a criação do token
    token_data = http_request.post("http://localhost:5000/token", json={"username": username, "password": password})
    if token_data.status_code != 200:
        return render_template("error.html", message="Bad username or password")
    # recupera o token
    response = jsonify({"success": True})
    set_access_cookies(response, token_data.json()['token'], max_age=60*60*24*7)
    return response

from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route("/content", methods=["GET"])
@jwt_required()
def content():
    return render_template("content.html")

@app.route("/error", methods=["GET"])
def error():
    return render_template("error.html")

# Adicionando as rotas CRUD para a entidade User
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return_users = []
    for user in users:
        return_users.append(user.serialize())
    return jsonify(return_users)

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    return jsonify(user.serialize())

@app.route("/users", methods=["POST"])
def create_user():
    email = request.form.get("email")
    password = request.form.get("password")
    print(email, password)
    user = User(name=email, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize())

@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.json
    user = User.query.get(id)
    user.name = data["name"]
    user.email = data["email"]
    user.password = data["password"]
    db.session.commit()
    return jsonify(user.serialize())

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(user.serialize())

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
@app.route("/token", methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    # Query your database for username and password
    user = User.query.filter_by(email=username, password=password).first()
    if user is None:
        # the user was not found on the database
        return jsonify({"msg": "Bad username or password"}), 401
    
    # create a new token with the user id inside
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id })

@app.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()  # Get the user ID from the JWT token
    tasks = Task.query.filter_by(user_id=user_id).all()
    return_tasks = []
    for task in tasks:
        return_tasks.append(task.serialize())
    return jsonify(return_tasks)

@app.route("/tasks/<int:id>", methods=["GET"])
@jwt_required()
def get_task(id):
    user_id = get_jwt_identity()  # Get the user ID from the JWT token
    task = Task.query.filter_by(id=id, user_id=user_id).first()
    if task is None:
        return jsonify({"error": "Task not found or unauthorized access"}), 404
    return jsonify(task.serialize())

@app.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    print(request.json)
    user_id = get_jwt_identity() # Get the user ID from the JWT token
    data = request.json
    task = Task(title=data["title"], status=data["status"], user_id=user_id)
    db.session.add(task)
    db.session.commit()
    
    # Print the HTTP cookies
    print(request.cookies)
    
    return jsonify(task.serialize())

@app.route("/tasks/<int:id>", methods=["PUT"])
@jwt_required()
def update_task(id):
    user_id = get_jwt_identity()  # Get the user ID from the JWT token
    data = request.json
    task = Task.query.filter_by(id=id, user_id=user_id).first()
    if task is None:
        return jsonify({"error": "Task not found or unauthorized access"}), 404
    task.title = data["title"]
    task.status = data["status"]
    db.session.commit()
    return jsonify(task.serialize())

@app.route("/tasks/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_task(id):
    user_id = get_jwt_identity()  # Get the user ID from the JWT token
    task = Task.query.filter_by(id=id, user_id=user_id).first()
    if task is None:
        return jsonify({"error": "Task not found or unauthorized access"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify(task.serialize())