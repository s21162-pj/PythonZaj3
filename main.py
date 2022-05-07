import getpass
import os
import sqlite3
import sys

from database import database
from rooms import rooms_service
from users import users_service


def register_user(db):
    login = input("Login:")
    password = getpass.getpass("Password:")
    if not users_service.validate_login(login):
        print("Wrong login!")
        return
    if not users_service.validate_password(password):
        print("Wrong password!")
        return

    if users_service.has_user(db, login):
        print("User exists!")
        return

    users_service.create_user(db, login, password)

def login(db):
    login = input("Login:")
    password = getpass.getpass("Password:")

    return users_service.login(db, login, password)


def list_users(db, filter=None):
    for user in users_service.get_all_users(db):
        if filter is None:
            print(user.login)
        elif user.login.find(filter) > -1:
            print(user.login)


def remove_user(db):
    login = input("Login to remove:")
    password = getpass.getpass("Password to remove:")

    return users_service.remove_user(db, login, password)

def delete_room(db):
    id = input("Room id to delete: ")
    password = getpass.getpass("Room to delete password: ")
    return rooms_service.delete_room_by_id(db, id, password)

def create_room(db, user):
    subject = input("Room's subject: ")
    rooms_service.create_room(db, user.login, getpass.getpass('Room password: '), subject)

def change_room_subject(db, user):
    id = input("Room id to change subject: ")
    subject = input("Room's new subject: ")
    rooms_service.change_subject(db, id, user.login, getpass.getpass('Room password:'), subject)

#przerzucić do database.py
def initialize_db():
    os.remove("sqllitedb.db")

    sql = sqlite3.connect("sqllitedb.db")
    cursor = sql.cursor()
    cursor.execute('''
                                                    CREATE TABLE IF NOT EXISTS rooms (
                                                        room_id integer integer PRIMARY KEY,
                                                        password text NOT NULL UNIQUE,
                                                        owner text NOT NULL,
                                                        subject text
                                                    )
                                                ''')
    cursor.execute('''
                                    CREATE TABLE IF NOT EXISTS users (
                                        user_id integer PRIMARY KEY,
                                        login text NOT NULL UNIQUE,
                                        password text NOT NULL
                                    )
                                ''')
    cursor.execute('''
                                    CREATE TABLE IF NOT EXISTS joins (
                                        room_id INTEGER,
                                        login text NOT NULL,
                                        FOREIGN KEY (room_id) REFERENCES rooms(room_id)
                                        FOREIGN KEY (login) REFERENCES users(login)
                                    )
                                ''')

    sql.commit()
    sql.close()

def join_room(db, user):
    id = input("Room id to join:" )
    rooms_service.join_room(user.login, id, getpass.getpass("Password: "))


def run():
    db = database.get_db("sqllitedb.db")

    menu1 = int(input("Select: 1 - rooms   2 - users   7 - delete database and create new one:"))
    if menu1 == 1:
        user = login(db)
        if user is None:
            print("Wrong credentials!")
            return
        menu5 = int(input("1 - create room   2 - delete room   3 - join room   4 - change room's subject"))
        if menu5 == 1:
            create_room(db, user)
        if menu5 == 2:
            delete_room(db)
        if menu5 == 3:
            join_room(db, user)
        if menu5 == 4:
            change_room_subject(db, user)
    if menu1 == 2:
        menu2 = int(input("Users menu \n  1 - login  2 - register"))
        if menu2 == 1:
            user = login(db)
            if user is None:
                print("Wrong credentials!")
                return
            menu3 = int(input("  1 - list all users   2 - delete user"))
            if menu3 == 1:
                users_service.get_all_users()
            if menu3 == 2:
                remove_user(db)

        elif menu2 == 2:
            register_user(db)
    if menu1 == 7:
        initialize_db()


if __name__ == '__main__':
    run()