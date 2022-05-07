import bcrypt

from database.database import Database
from database.rooms_model import Room


def create_room(db: Database, owner_login: str, password: str, subject: str):
    #rooms = db.find_all_in_db('ROOM')
    rooms = db.find_all_rooms_in_db()

    #new_id = 0 if len(rooms) == 0 else str(int(rooms[-1][1]) + 1)
    new_id = len(rooms)
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    db.put_room_to_db(new_id, owner_login, password, subject)


def get_room(db: Database, id: str):
    #db_room = db.find_in_db('ROOM', id)
    db_room = db.find_all_rooms_in_db(id)
    if db_room is None:
        return None

    #return Room(id=db_room[1], owner=db_room[2], password=db_room[3])
    return Room(id=db_room[1], owner=db_room[2], password=db_room[3], subject=db_room[4])

def change_subject(db: Database, id:str, owner_login: str, password: str, subject: str):
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    #db_room = db.find_all_rooms_in_db(id)
    #if db_room is None:
    #    return None
    db.change_subject(subject, id, owner_login)
"""
def delete_room_by_id(db: Database, id: str):
    #db.remove_from_db('ROOM', id)
    #db.remove_from_db('JOIN', id)
    db.remove_room_from_db(id)
"""
def delete_room_by_id(db: Database, id: str, password: str):
    #db.remove_from_db('ROOM', id)
    #db.remove_from_db('JOIN', id)
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    db.remove_room_from_db(id, password)



def join_room(db: Database, user_login: str, id: str, password: str):
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    db.find_room_in_db(id, password)
    if db.find_room_in_db(id, password) is True:
        db.join_to_room(id, user_login)
    else:
        return False

'''
def join_room(db: Database, user_login: str, id: str, password: str) -> bool:
    room = get_room(db, id)
    if room is None:
        return False

    if not bcrypt.checkpw(password.encode('utf-8'), room.password.encode('utf-8')):
        return False

    db.put_to_db('JOIN', id, user_login)
    return True'''