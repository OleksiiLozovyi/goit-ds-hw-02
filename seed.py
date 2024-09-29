import sqlite3 as sql
from sqlite3 import Error
from contextlib import contextmanager
import faker

database = './hw2.db'


@contextmanager
def create_connection(db_file):
    cnct = None
    try:
        cnct = sql.connect(db_file)
        yield cnct
        cnct.commit()
    except Error as e:
        if cnct:
            cnct.rollback()
        print(f"Error: {e}")
    finally:
        if cnct:
            cnct.close()


def update_users(cnct, user):
    sql_query = """
    INSERT INTO users (fullname, email) VALUES (?, ?);
    """
    cur = cnct.cursor()
    try:
        cur.execute(sql_query, user)
    except Error as e:
        print(f"Failed to insert user: {e}")


def insert_status(cnct, status):
    sql_query = """
    INSERT INTO status (name) VALUES (?);
    """
    cur = cnct.cursor()
    try:
        cur.execute(sql_query, (status,))
    except Error as e:
        print(f"Failed to insert status: {e}")


def insert_tasks(cnct, task):
    sql_query = """
    INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?);
    """
    cur = cnct.cursor()
    try:
        cur.execute(sql_query, task)
    except Error as e:
        print(f"Failed to insert task: {e}")


if __name__ == '__main__':
    with create_connection(database) as conn:
        fake_data = faker.Faker()

        status_list = ['new', 'in progress', 'completed']
        for status in status_list:
            insert_status(conn, status)

        for i in range(5):
            fake_name = fake_data.name()
            fake_email = fake_data.email()
            user = (fake_name, fake_email)
            update_users(conn, user)

        for i in range(5):
            title = fake_data.sentence()
            description = fake_data.text()
            status_id = fake_data.random_int(min=1, max=len(status_list))
            user_id = fake_data.random_int(min=1, max=5)
            task = (title, description, status_id, user_id)
            insert_tasks(conn, task)
