from flask import Flask, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from .routes import some_blueprint 
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@db:5432/your_db_name'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)  

    from .routes import some_blueprint
    app.register_blueprint(some_blueprint)

    return app

app = create_app()  

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Routes
@app.route('/')
def home():
    if 'user_id' in session:
        return jsonify({'message': 'Welcome back!'}), 200
    return jsonify({'message': 'Please login'}), 401

# Authentication
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'message': 'Username already exists!'}), 409  # Conflict error if user exists
    
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        session['user_id'] = user.id
        return jsonify({'message': 'Logged in successfully!'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully!'}), 200

# User CRUD
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username} for user in users]), 200

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user.username = data.get('username', user.username)
    db.session.commit()
    return jsonify({'message': 'User updated successfully!'}), 200

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully!'}), 200

# Task CRUD
@app.route('/tasks', methods=['POST'])
def create_task():
    if 'user_id' not in session:
        return jsonify({'message': 'Login required'}), 401
    data = request.json
    new_task = Task(title=data['title'], user_id=session['user_id'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully!'}), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    if 'user_id' not in session:
        return jsonify({'message': 'Login required'}), 401
    tasks = Task.query.filter_by(user_id=session['user_id']).all()
    return jsonify([{'id': task.id, 'title': task.title, 'completed': task.completed} for task in tasks]), 200

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    if 'user_id' not in session:
        return jsonify({'message': 'Login required'}), 401
    data = request.json
    task = Task.query.get(id)
    if not task or task.user_id != session['user_id']:
        return jsonify({'message': 'Task not found'}), 404
    task.title = data.get('title', task.title)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify({'message': 'Task updated successfully!'}), 200

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    if 'user_id' not in session:
        return jsonify({'message': 'Login required'}), 401
    task = Task.query.get(id)
    if not task or task.user_id != session['user_id']:
        return jsonify({'message': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully!'}), 200

# Dashboard
@app.route('/dashboard', methods=['GET'])
def dashboard():
    user_count = User.query.count()
    task_count = Task.query.count()
    completed_tasks = Task.query.filter_by(completed=True).count()
    return jsonify({
        'total_users': user_count,
        'total_tasks': task_count,
        'completed_tasks': completed_tasks
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
