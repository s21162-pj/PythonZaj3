import os
import re
import sqlite3
from typing import List

import bcrypt

from database.database import Database
from database.users_model import User

LOGIN_RE = r'^[a-zA-Z0-9]+$'

def validate_login(login: str):
    if not len(login) > 3:
        return False

    return re.match(LOGIN_RE, login) is not None


def validate_password(password):
    return len(password) > 4


def has_user(db: Database, login: str):
    return db.find_user_in_db(login.lower()) is not None


def login(db: Database, login: str, password: str):
    #user = db.find_in_db('USER', login.lower())
    user = db.find_user_in_db(login.lower())
    if user is None:
        return None

    if not bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
        return None

    return User(login=user[1])


def create_user(db: Database, login: str, password):
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    #db.put_to_db('USER', login.lower(), password)
    db.put_user_to_db(login.lower(), password)

#def get_all_users(db: Database) -> List[User]:
#    return [User(login=row[1]) for row in db.find_all_in_db('USER')]

def get_all_users():
    sql = sqlite3.connect("sqllitedb.db")
    cursor = sql.cursor()

    cursor.execute("SELECT * FROM users")

    rows = cursor.fetchall()
    for r in rows:
        print(r[1])
    sql.commit()
    sql.close()


def remove_user(db: Database, login: str, password):
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    #db.remove_from_db('USER', login.lower())
    db.remove_user_from_db(login.lower(), password)
