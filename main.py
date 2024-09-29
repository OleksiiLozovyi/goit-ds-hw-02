import sqlite3 as sql
from sqlite3 import Error
from contextlib import contextmanager


database = './hw2.db'

@contextmanager
def create_connection(db_file):
    cnct = sql.connect(db_file)
    yield cnct
    cnct.rollback()
    cnct.close()

def crete_table(cnct, create_table_sql):
    try:
        c = cnct.cursor()
        c.execute(create_table_sql)
        cnct.commit()
    except Error as e:
        print(e)

if __name__ == '__main__':
    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
    id integer PRIMARY KEY,
    fullname VARCHAR(100),
    email VARCHAR(100),
    CONSTRAINT users_email_un UNIQUE (email)
    );
    """

    sql_create_status_table = """
    CREATE TABLE IF NOT EXISTS status (
    id integer PRIMARY KEY,
    name VARCHAR(50),
    CONSTRAINT status_name_un UNIQUE (name)
    );
    """

    sql_create_tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
    id integer PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100),
    description text,
    status_id integer,
    user_id integer,
    FOREIGN KEY (status_id) REFERENCES status (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
    FOREIGN KEY (user_id) REFERENCES users (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
    );
    """
with create_connection(database) as cnct:

    if cnct is not None:
        crete_table(cnct, sql_create_users_table)
        crete_table(cnct, sql_create_status_table)
        crete_table(cnct, sql_create_tasks_table)
    else:
        print("Cannot create a connection to DB")