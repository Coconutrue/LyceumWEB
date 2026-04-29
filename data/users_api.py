import flask
from flask import jsonify, make_response, request
from unicodedata import category

from data import db_session
from data.users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    user = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'email', 'name', 'created_date', 'is_admin'))
                 for item in user]
        }
    )

@blueprint.route('/api/users/<int:id>', methods=['GET'])
def get_one_user(id):
    db_sess = db_session.create_session()
    user = db_sess.get(User, id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'user': user.to_dict(only=(
                'id','email', 'name', 'created_date', 'is_admin'))
        }
    )

@blueprint.route('/api/users', methods=['POST'])
def create_news():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['name', 'email', 'id', 'is_admin', 'created_date']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    users = User(
        email=request.json['email'],
        name=request.json['name'],
        user_id=request.json['user_id'],
        category=request.json['category']
    )
    db_sess.add(users)
    db_sess.commit()
    return jsonify({'id': users.id})

# @blueprint.route('/api/news/<int:news_id>', methods=['DELETE'])
# def delete_news(news_id):
#     db_sess = db_session.create_session()
#     news = db_sess.get(News, news_id)
#     if not news:
#         return make_response(jsonify({'error': 'Not found'}), 404)
#     db_sess.delete(news)
#     db_sess.commit()
#     return jsonify({'success': 'OK'})