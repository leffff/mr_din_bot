import psycopg2
import json

# считываем конфиг
with open('config.json') as f:
    config = json.loads(f.read())
    PASSWORD = config["PASSWORD"]
    DBNAME = config["DBNAME"]
    USER = config["USER"]
    HOST = config["HOST"]
    PORT = config["PORT"]


# Первое создание базы данных
def first_db_creation():
    '''
    return {"result": "ok"}
    return {"result": "database already exists"}
    return {"result": "unknown error"}
    '''

    conn = psycopg2.connect(dbname=DBNAME, user=USER,
                            password=PASSWORD, host=HOST, port=PORT)
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE TABLE users ("
                       "user_id INT PRIMARY KEY NOT NULL, "
                       "tg_nickname VARCHAR(30) NOT NULL UNIQUE, "
                       "name VARCHAR(30) NOT NULL, "
                       "surname VARCHAR(30) NOT NULL, "
                       "qualification text NOT NULL, "
                       "experience INT NOT NULL, "
                       "qualities text NOT NULL,"
                       "city VARCHAR(30) NOT NULL)")
        conn.commit()
        cursor.execute("CREATE TABLE cancellations ("
                       "cancellation_id SERIAL PRIMARY KEY NOT NULL, "
                       "employer_self BOOL DEFAULT FALSE, "
                       "employer_other BOOL DEFAULT FALSE, "
                       "worker_self BOOL DEFAULT FALSE, "
                       "worker_other BOOL DEFAULT FALSE)")
        conn.commit()
        cursor.execute("CREATE TABLE orders ("
                       "order_id SERIAL PRIMARY KEY NOT NULL, "
                       "employer_id SERIAL REFERENCES users(user_id) NOT NULL,"
                       "worker_id SERIAL REFERENCES users(user_id),"
                       "title VARCHAR(40) NOT NULL, "
                       "description TEXT NOT NULL, "
                       "payment REAL NOT NULL, "
                       "active BOOLEAN DEFAULT True NOT NULL, "
                       "start_time INT, "
                       "finish_time INT,"
                       "mark INT,"
                       "feedback TEXT,"
                       "cancellation_id SERIAL REFERENCES cancellations(cancellation_id))")
        conn.commit()
    except psycopg2.errors.DuplicateTable:
        return {"result": "database already exists"}
    except Exception as ex:
        return {"result": f"unknown error: {ex.args[0]}"}
    else:
        return {"result": "ok"}
