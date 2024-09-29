import sqlite3 as sql
from sqlite3 import Error
from contextlib import contextmanager

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


def get_tasks_for_user(cnct, user_id):
    sql_query = "SELECT * FROM tasks WHERE user_id = ?"
    cur = cnct.cursor()
    cur.execute(sql_query, (user_id,))
    return cur.fetchall()


def get_tasks_by_status(cnct, status_name):
    sql_query = """
    SELECT * FROM tasks 
    WHERE status_id = (SELECT id FROM status WHERE name = ?);
    """
    cur = cnct.cursor()
    cur.execute(sql_query, (status_name,))
    return cur.fetchall()


def update_task_status(cnct, task_id, new_status):
    sql_query = """
    UPDATE tasks 
    SET status_id = (SELECT id FROM status WHERE name = ?) 
    WHERE id = ?;
    """
    cur = cnct.cursor()
    cur.execute(sql_query, (new_status, task_id))


def get_users_without_tasks(cnct):
    sql_query = """
    SELECT * FROM users 
    WHERE id NOT IN (SELECT user_id FROM tasks);
    """
    cur = cnct.cursor()
    cur.execute(sql_query)
    return cur.fetchall()


def add_task_for_user(cnct, title, description, status_id, user_id):
    sql_query = """
    INSERT INTO tasks (title, description, status_id, user_id) 
    VALUES (?, ?, ?, ?);
    """
    cur = cnct.cursor()
    cur.execute(sql_query, (title, description, status_id, user_id))


def get_unfinished_tasks(cnct):
    sql_query = """
    SELECT * FROM tasks 
    WHERE status_id != (SELECT id FROM status WHERE name = 'completed');
    """
    cur = cnct.cursor()
    cur.execute(sql_query)
    return cur.fetchall()


def delete_task(cnct, task_id):
    sql_query = "DELETE FROM tasks WHERE id = ?"
    cur = cnct.cursor()
    cur.execute(sql_query, (task_id,))


def find_users_by_email(cnct, email_pattern):
    sql_query = "SELECT * FROM users WHERE email LIKE ?"
    cur = cnct.cursor()
    cur.execute(sql_query, (email_pattern,))
    return cur.fetchall()


def update_user_name(cnct, user_id, new_name):
    sql_query = "UPDATE users SET fullname = ? WHERE id = ?"
    cur = cnct.cursor()
    cur.execute(sql_query, (new_name, user_id))


def count_tasks_by_status(cnct):
    sql_query = """
    SELECT status.name, COUNT(tasks.id) AS task_count
    FROM tasks 
    JOIN status ON tasks.status_id = status.id 
    GROUP BY status.name;
    """
    cur = cnct.cursor()
    cur.execute(sql_query)
    return cur.fetchall()


def get_tasks_by_email_domain(cnct, domain_pattern):
    sql_query = """
    SELECT u.* 
    FROM tasks t
    JOIN users u ON t.user_id = u.id 
    WHERE u.email LIKE ?;
    """
    cur = cnct.cursor()
    cur.execute(sql_query, (domain_pattern,))
    return cur.fetchall()


def get_tasks_without_description(cnct):
    sql_query = "SELECT * FROM tasks WHERE description IS NULL"
    cur = cnct.cursor()
    cur.execute(sql_query)
    return cur.fetchall()


def get_users_and_tasks_in_progress(cnct):
    sql_query = """
    SELECT users.fullname as UserName, tasks.title as Title, tasks.description as Description
    FROM tasks 
    JOIN users ON tasks.user_id = users.id 
    JOIN status ON tasks.status_id = status.id 
    WHERE status.name = 'in progress';
    """
    cur = cnct.cursor()
    cur.execute(sql_query)
    return cur.fetchall()


def get_users_task_count(cnct):
    sql_query = """
    SELECT users.fullname as UserName, COUNT(tasks.id) AS task_count 
    FROM users 
    LEFT JOIN tasks ON users.id = tasks.user_id 
    GROUP BY users.fullname;
    """
    cur = cnct.cursor()
    cur.execute(sql_query)
    return cur.fetchall()


if __name__ == '__main__':
    with create_connection(database) as conn:
        user_tasks = get_tasks_for_user(conn, 2)
        print("Tasks for user 2:", user_tasks)

        new_tasks = get_tasks_by_status(conn, 'new')
        print("Tasks':", new_tasks)

        update_task_status(conn, 1, 'in progress')

        users_without_tasks = get_users_without_tasks(conn)
        print("Users without tasks:", users_without_tasks)

        add_task_for_user(conn, "New Task", "Description for new task", 1, 1)

        unfinished_tasks = get_unfinished_tasks(conn)
        print("Unfinished tasks:", unfinished_tasks)

        delete_task(conn, 1)

        users_with_email = find_users_by_email(conn, "%@example.com")
        print("Users with email pattern:", users_with_email)

        update_user_name(conn, 1, "New Name")

        task_count_by_status = count_tasks_by_status(conn)
        print("Task count by status:", task_count_by_status)

        tasks_by_domain = get_tasks_by_email_domain(conn, "%@example.com")
        print("Tasks for users with email domain '@example.com':", tasks_by_domain)

        tasks_without_desc = get_tasks_without_description(conn)
        print("Tasks without description:", tasks_without_desc)

        users_tasks_in_progress = get_users_and_tasks_in_progress(conn)
        print("Users and their tasks in 'in progress':", users_tasks_in_progress)

        users_task_count = get_users_task_count(conn)
        print("Users and their task count:", users_task_count)
