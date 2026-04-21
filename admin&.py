import sys
from data import db_session
from data.users import User

def make_admin(email):
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter_by(email=email).first()

    if not user:
        print("нет такого пользователя. Прочекай бдшку")

    user.is_admin = True
    db_sess.commit()
    print("Админка накинута")
    return True


if __name__ == "__main__":
    email = input("поиск по почте. Вводи").strip()

    make_admin(email)