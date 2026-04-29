from requests import get, post, delete

# print(get('http://127.0.0.1:2010/api/news').json())
# print(get('http://127.0.0.1:2010/api/news/2').json())
#
# print(get('http://127.0.0.1:2010/api/news/999').json())
# print(get('http://127.0.0.1:2010/api/news/w').json())
# print(post('http://127.0.0.1:2010/api/news', json={}).json())
# print(post('http://127.0.0.1:2010/api/news',
#            json={'title': 'Заголовок'}).json())
#
# print(post('http://127.0.0.1:2010/api/news',
#            json={'title': 'Заголовок',
#                  'content': 'Текст новости',
#                  'user_id': 1,
#                  'category': 'other'}).json())Ы
# print(delete('http://127.0.0.1:2010/api/news/999').json())
# print(delete('http://127.0.0.1:2010/api/news/4').json())
print(get('http://127.0.0.1:2010/api/users/1').json())
