import csv
import os
import sqlite3
import tempfile


class Database:
    def __init__(self, connection):
        self.connection = connection
        self.cur = connection.cursor()
        #dopisać
        #self.create_tables()


    def init(self):
        self._check_db_exists()

    def initialize_db(self):
        os.remove("sqllitedb.db")

        self.cur.execute('''
                                                        CREATE TABLE IF NOT EXISTS rooms (
                                                            room_id integer integer PRIMARY KEY,
                                                            password text NOT NULL UNIQUE,
                                                            owner text NOT NULL
                                                        )
                                                    ''')
        self.cur.execute('''
                                        CREATE TABLE IF NOT EXISTS users (
                                            user_id integer PRIMARY KEY,
                                            login text NOT NULL UNIQUE,
                                            password text NOT NULL
                                        )
                                    ''')

        self.connection.commit()

    def put_to_db(self, entry_type, *values):
        with open(self.path, "a", newline="") as csvfile:
            writer = self._get_writer(csvfile)
            writer.writerow([entry_type] + list(values))


    def put_user_to_db(self, *values):
        self.cur.execute("CREATE TABLE IF NOT EXISTS users (user_id integer PRIMARY KEY,login text NOT NULL UNIQUE,password text NOT NULL)")
        self.cur.execute("INSERT INTO users (login, password) VALUES(?,?)", list(values))
        self.connection.commit()
        #sql.close()

    def put_room_to_db(self, *values):
        self.cur.execute("CREATE TABLE IF NOT EXISTS rooms (room_id integer integer PRIMARY KEY,password text NOT NULL UNIQUE,owner text NOT NULL, subject text NOT NULL)")
        self.cur.execute("INSERT INTO rooms (room_id, owner, password, subject) VALUES(?,?,?,?)", list(values))

        self.connection.commit()

    def join_to_room(self, *values):
        self.cur.execute('''
                                    CREATE TABLE IF NOT EXISTS joins (
                                        room_id INTEGER,
                                        login text NOT NULL,
                                        FOREIGN KEY (room_id) REFERENCES rooms(room_id)
                                        FOREIGN KEY (login) REFERENCES users(login)
                                    )
                                ''')
        self.cur.execute("INSERT INTO joins (room_id, login) VALUES(?,?)", list(values))
        self.connection.commit()

    def change_subject(self, *values):
        self.cur.execute("UPDATE rooms SET subject=? WHERE room_id = ? AND owner = ?", list(values))
        self.connection.commit()

    def remove_user_from_db(self, login, password):
        self.cur.execute("DELETE FROM users WHERE (login)=(?)", [login])
        self.connection.commit()

    def remove_room_from_db(self, id, password):
        self.cur.execute("DELETE FROM rooms WHERE (room_id) = (?)", [id])
        self.connection.commit()

    def find_user_in_db(self, *values):
        self.cur.execute("SELECT * FROM users WHERE login =(?)", list(values))
        rows = self.cur.fetchall()
        for row in rows:
            return row
        return None
        self.connection.commit()

    def find_room_in_db(self, *values):
        self.cur.execute("SELECT * FROM rooms WHERE (room_id, password) = (?,?)", list(values))
        rows = self.cur.fetchall()
        for row in rows:
            return True
        return False
        self.connection.commit()

    def find_all_rooms_in_db(self, *values):
        self.cur.execute("SELECT * FROM rooms")
        self.connection.commit()
        row = self.cur.fetchall()
        if self._match(row, *values):
            return row

    def _check_db_exists(self):
       try:
           os.stat(self.path)
       except FileNotFoundError:
           f = open(self.path, "w")
           f.close()

    def _match(self, row, *values):
       # if row[0] != entry_type:
        #    return False

        for index, value in enumerate(values):
            if value is None:
                continue

            if row[index + 1] != value:
                return False

        return True

    def _get_reader(self, file):
        return csv.reader(file, delimiter=",", quotechar="|")

    def _get_writer(self, file):
        return csv.writer(file, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)

def get_db(path):
    connection = sqlite3.connect(path)
    #db.init()
    return Database(connection)