import os

from flask import request, jsonify, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from data import db_session
from data.users import User
from main import app

blueprint = Blueprint('auth_api', __name__, template_folder='templates')


@blueprint.route('/api/register', methods=['POST'])
def user_register():
    if not request.json:
        return jsonify({'error': 'Empty request'}), 400
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    if not all([name, email, password]):
        return jsonify({'error': 'Missing fields: name, email, password required'}), 400
    if len(name) < 3 or len(name) > 14:
        return jsonify({'error': 'Name must be 3-14 characters'}), 400
    if len(password) < 3 or len(password) > 14:
        return jsonify({'error': 'Password must be 3-14 characters'}), 400
    if '@' not in email:
        return jsonify({'error': 'Invalid email'}), 400
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.email == email).first():
        return jsonify({'error': 'Email already exists'}), 400
    if db_sess.query(User).filter(User.name == name).first():
        return jsonify({'error': 'Username already exists'}), 400
    user = User(name=name, email=email)
    user.set_password(password)
    db_sess.add(user)
    db_sess.commit()
    login_user(user)
    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'is_admin': user.is_admin
        }
    }), 201


@blueprint.route('/api/login', methods=['POST'])
def user_login():
    if not request.json:
        return jsonify({'error': 'Empty request'}), 400
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401
    login_user(user)
    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'is_admin': user.is_admin
        }
    })


@blueprint.route('/api/logout', methods=['POST'])
@login_required
def user_logout():
    logout_user()
    return jsonify({'success': True})


@blueprint.route('/api/user/<string:user_name>', methods=['GET'])
def api_get_user(user_name):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == user_name).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'is_admin': user.is_admin,
        'created_date': user.created_date.isoformat() if user.created_date else None
    })


@blueprint.route('/api/user', methods=['PUT'])
@login_required
def api_update_user():
    if not request.json:
        return jsonify({'error': 'Empty request'}), 400
    data = request.json
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    new_name = data.get('name')
    if new_name and new_name != user.name:
        if len(new_name) < 3 or len(new_name) > 14:
            return jsonify({'error': 'Name must be 3-14 characters'}), 400
        existing = db_sess.query(User).filter(User.name == new_name).first()
        if existing and existing.id != user.id:
            return jsonify({'error': 'Username already exists'}), 400
        user.name = new_name
    new_email = data.get('email')
    if new_email and new_email != user.email:
        if '@' not in new_email:
            return jsonify({'error': 'Invalid email'}), 400
        existing = db_sess.query(User).filter(User.email == new_email).first()
        if existing and existing.id != user.id:
            return jsonify({'error': 'Email already exists'}), 400
        user.email = new_email
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')
    if new_password:
        if not old_password:
            return jsonify({'error': 'Old password required to change password'}), 400
        if not user.check_password(old_password):
            return jsonify({'error': 'Invalid old password'}), 400
        if new_password != confirm_password:
            return jsonify({'error': 'New passwords do not match'}), 400
        if len(new_password) < 3 or len(new_password) > 14:
            return jsonify({'error': 'Password must be 3-14 characters'}), 400
        user.set_password(new_password)
    db_sess.commit()
    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'is_admin': user.is_admin
        }
    })






# @blueprint.route('/api/admin/users', methods=['GET'])
# @login_required
# def admin_get_users():
#     if not current_user.is_admin:
#         return jsonify({'error': 'Admin access required'}), 403
#     db_sess = db_session.create_session()
#     users = db_sess.query(User).all()
#     return jsonify({
#         'users': [{
#             'id': u.id,
#             'name': u.name,
#             'email': u.email,
#             'is_admin': u.is_admin,
#             'created_date': u.created_date.isoformat() if u.created_date else None,
#             'news_count': len(u.news)
#         } for u in users]
#     })
#
#
# @blueprint.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
# @login_required
# def admin_delete_user(user_id):
#     if not current_user.is_admin:
#         return jsonify({'error': 'Admin access required'}), 403
#     if user_id == current_user.id:
#         return jsonify({'error': 'Cannot delete yourself'}), 400
#     db_sess = db_session.create_session()
#     user = db_sess.get(User, user_id)
#     if not user:
#         return jsonify({'error': 'User not found'}), 404
#     for news in user.news:
#         if news.image:
#             image_path = os.path.join(app.config['NEWS_UPLOAD_FOLDER'], news.image.split('/')[-1])
#             if os.path.exists(image_path):
#                 os.remove(image_path)
#         db_sess.delete(news)
#     db_sess.delete(user)
#     db_sess.commit()
#     return jsonify({'success': True, 'message': f'User {user.name} deleted'})