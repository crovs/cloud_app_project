from flask import Blueprint, request, jsonify
from .models import User, db


main = Blueprint('main', __name__)

@main.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201


@main.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users])

@main.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    if user:
        user.name = data['name']
        user.email = data['email']
        db.session.commit()
        return jsonify({'message': 'User updated!'})
    return jsonify({'message': 'User not found'}), 404

@main.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted!'})
    return jsonify({'message': 'User not found'}), 404
