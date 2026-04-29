import flask
from flask import jsonify, make_response, request
from unicodedata import category

from data import db_session
from data.News import News

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/news')
def get_news():
    db_sess = db_session.create_session()
    news = db_sess.query(News).all()
    return jsonify(
        {
            'news':
                [item.to_dict(only=('title', 'content', 'user.name', 'created_date', 'category', 'image', 'id'))
                 for item in news]
        }
    )

@blueprint.route('/api/news/<int:id>', methods=['GET'])
def get_one_news(id):
    db_sess = db_session.create_session()
    news = db_sess.get(News, id)
    if not news:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'news': news.to_dict(only=(
                'title', 'content', 'user_id', 'created_date', 'category', 'image'))
        }
    )

@blueprint.route('/api/news', methods=['POST'])
def create_news():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id', 'category']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    news = News(
        title=request.json['title'],
        content=request.json['content'],
        user_id=request.json['user_id'],
        category=request.json['category']
    )
    db_sess.add(news)
    db_sess.commit()
    return jsonify({'id': news.id})

@blueprint.route('/api/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    db_sess = db_session.create_session()
    news = db_sess.get(News, news_id)
    if not news:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(news)
    db_sess.commit()
    return jsonify({'success': 'OK'})