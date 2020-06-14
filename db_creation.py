import sqlite3

from create_environment import create_environment
# from os import getenv

create_environment()

# DBNAME = getenv("DBNAME")


# Первое создание базы данных
'''
Первое создание базы данных.
return {"result": "ok"}
return {"result": "database already exists"}
return {"result": "unknown error"}
'''


def first_db_creation():
    try:
        with sqlite3.connect(DBNAME) as conn:
            cursor = conn.cursor()

            cursor.execute("CREATE TABLE users ("
                           "user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
                           "tg_nickname VARCHAR(30) NOT NULL UNIQUE, "
                           "tg_id INT NOT NULL UNIQUE,"
                           "name VARCHAR(30) NOT NULL, "
                           "surname VARCHAR(30) NOT NULL, "
                           "qualification text NOT NULL, "
                           "category VARCHAR(30) NOT NULL,"
                           "experience INT NOT NULL);")

            cursor.execute("CREATE TABLE orders ("
                           "order_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
                           "employer_id INTEGER REFERENCES users(user_id) NOT NULL,"
                           "worker_id INTEGER REFERENCES users(user_id),"
                           "title VARCHAR(40) NOT NULL, "
                           "description TEXT NOT NULL, "
                           "category VARCHAR(30) NOT NULL,"
                           "worker_skills text NOT NULL,"
                           "active BOOLEAN DEFAULT True NOT NULL, "
                           "start_time INT,"
                           "finish_time INT,"
                           "time INT,"
                           "mark INT,"
                           "feedback TEXT,"
                           "result INT,"
                           "active_orders INT)")
            conn.commit()
            return {"status": "ok"}
    except Exception as ex:
        return {"status": f"unknown error: {ex.args[0]}"}
    finally:
        conn.close()
