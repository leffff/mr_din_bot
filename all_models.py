import psycopg2
import create_environment
from os import getenv

DBNAME = getenv("DBNAME")
USER = getenv("USER")
PASSWORD = getenv("PASSWORD")
PORT = getenv("PORT")
HOST = getenv("HOST")


class User:
    def __init__(self, tg_nickname: str):
        self.tg_nickname = tg_nickname

    # добавление нового пользователя
    '''входной словарь: 
    {"tg_nickname": "str(30)", 
    "name": "str(30)", 
    "surname": "str(30)", 
    "qualification": "str, str",
    "qualities": "str, str",
    "experience": "int",
    "city": "str(30)"}

    На выход:
     {"status": "ok"}
    {"status": wrong type}
    {'status': error_type}
    '''

    @staticmethod
    def add_user(user_data: dict):
        tg_nickname = user_data["tg_nickname"]
        name = user_data["name"]
        surname = user_data["surname"]
        qualification = user_data["qualification"]
        experience = user_data["experience"]
        qualities = user_data["qualities"]
        city = user_data["city"]
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    assert type(
                        tg_nickname) == str, f"invalid type for tg_nickname, expected str got {type(tg_nickname)}"
                    assert type(name) == str, f"invalid type for name, expected str got {type(name)}"
                    assert type(surname) == str, f"invalid type for surname, expected str got {type(surname)}"
                    assert type(
                        qualification) == str, f"invalid type for qualification, expected str got {type(qualification)}"
                    assert type(experience) == int, f"invalid type for experience expected int got {type(experience)}"
                    assert type(qualities) == str, f"invalid type for qualities, expected str got {type(qualities)}"
                    assert type(city) == str, f"invalid type for city, expected str got {type(city)}"
                    cursor.execute(
                        'INSERT INTO users(tg_nickname, name, surname, qualification, experience, qualities, city) '
                        'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (tg_nickname, name, surname, qualification, experience, qualities, city))
                    conn.commit()
                    return {"status": "ok"}
        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()

    '''
    Функция для поиска пользователей по qualification.
    На выход:
    {"status": "ok", "output": (User(), User()...)}
    {"status": "users not found"}
    {'status': error_type}
    '''

    @staticmethod
    def get_user_by_qualification(qualification) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    assert type(
                        qualification) == str, f"invalid type for qualification, expected str got {type(qualification)}"
                    cursor.execute('SELECT tg_nickname FROM users WHERE qualification = %s', (qualification,))
                    nicknames = cursor.fetchall()
                    if nicknames:
                        conn.commit()
                        data = tuple(User(nickname) for nickname in nicknames)
                        return {"status": "ok", "output": data}
                    return {"status": "users not found"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    '''
    Функция для поиска пользователя по id.
    На выход:
    {"status": "ok", "output": User()}
    {"status": "users not found"}
    {'status': error_type}
    '''

    @staticmethod
    def get_user_by_id(user_id):
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    assert type(user_id) == int, f"invalid type for qualification, expected int got {type(user_id)}"
                    cursor.execute(f'SELECT tg_nickname FROM users WHERE user_id = %s', (user_id,))
                    nickname = cursor.fetchone()
                    if nickname:
                        conn.commit()
                        return {"status": "ok", "output": User(nickname)}
                    return {"status": "user not found"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    # Функция для получения name и surname пользователя
    def get_name_surname(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT name, surname FROM users WHERE tg_nickname = %s", (self.tg_nickname,))
                    out = cursor.fetchone()
                    if out:
                        conn.commit()
                        return {'status': "ok", "out": out}
                    return {"status": "error in query, result = False"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    # Функция для получения qualification пользователя
    def get_qualification(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT qualification FROM users WHERE tg_nickname = %s", (self.tg_nickname,))
                    out = cursor.fetchone()
                    if out:
                        conn.commit()
                        return {"status": "ok", "out": out[0]}
                    return {"status": "error in query, result = False"}

        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()

    # Функция для получения qualities пользователя
    def get_qualities(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT qualities FROM users WHERE tg_nickname = %s", (self.tg_nickname,))
                    out = cursor.fetchone()
                    if out:
                        conn.commit()
                        return {"status": "ok", "out": out[0]}
                    return {"status": "error in query, result = False"}

        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()

    # Функция для получения experience пользователя
    def get_experience(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT experience FROM users WHERE tg_nickname = %s", (self.tg_nickname,))
                    out = cursor.fetchone()
                    if out:
                        conn.commit()
                        return {"status": "ok", "out": out[0]}
                    return {"status": "error in query, result = False"}
        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()

    # Функция для получения id пользователя
    def get_user_id(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT user_id FROM users WHERE tg_nickname = %s", (self.tg_nickname,))
                    out = cursor.fetchone()
                    if out:
                        conn.commit()
                        return {"status": "ok", "out": out[0]}
                    return {"status": "error in query, result = False"}
        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()

    '''
    Функция для получения списка классов всех пользователей.
    На выход:
    {"status": "ok", "output": tuple(User(), User()...)}
    {"status": "no users in database"}
    '''

    @staticmethod
    def get_all_users() -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT tg_nickname FROM users")
                    out = cursor.fetchall()
                if out:
                    conn.commit()
                    data = tuple(User(i[0]) for i in out)
                    return {"status": "ok", "out": data}
                return {"status": "no users in database"}
        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()

    '''
    Функция для просмотра работ человека.
    На выход:
    {"status": "ok", "out": tuple(data)}
    {"status": "no works found"}
    '''

    def watch_my_works(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    user_id = User(self.tg_nickname).get_user_id()["out"]
                    cursor.execute("SELECT title FROM orders INNER JOIN users ON worker_id = %s", (user_id,))
                    orders = cursor.fetchall()
                    if orders:
                        conn.commit()
                        data = tuple(Order(title) for title in orders)
                        return {"status": "ok", "out": data}
                    return {"status": "no works found"}
        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()

    '''
    Функция для просмотра заказов человека.
    На выход:
    {"status": "ok", "out": tuple(Order(), Order()...)}
    {"status": "no orders found"}
    '''

    def watch_my_orders(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    user_id = User(self.tg_nickname).get_user_id()["out"]
                    cursor.execute("SELECT title FROM orders INNER JOIN users ON worker_id = %s", (user_id,))
                    orders = cursor.fetchall()
                    if orders:
                        data = tuple(Order(title) for title in orders)
                        return {"status": "ok", "out": data}
                    return {"status": "no orders found"}
        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()


'''
    Проверка title
    На выход:
    {"status": "ok"}
    {"status": "order not found"}
    {"status": wrong type}
    '''


def try_title(title: str) -> dict:
    try:
        with psycopg2.connect(dbname=DBNAME, user=USER,
                              password=PASSWORD, host=HOST, port=PORT) as conn:
            with conn.cursor() as cursor:
                assert type(title) == str, f"invalid type for title, expected str got {type(title)}"
                cursor.execute("SELECT order_id FROM orders WHERE title = %s", (title,))
                if cursor.fetchone():
                    conn.commit()
                    return {"status": "ok"}
                return {"status": "order not found"}
    except Exception as ex:
        return {"status": ex.args[0]}
    finally:
        conn.close()


class Order:
    def __init__(self, title: str):
        self.title = title

    # Добавление нового заказа
    '''Входной словарь:
    {"employer_id": int,
    "title": "str(40),
    "description": "str",
    "payment": float,
    "start_time": int}

    На выход:
    {"status": "ok"}
    {"status": wrong type}
    {'status': error_type}
    '''

    @staticmethod
    def add_order(order_data: dict) -> dict:
        employer_id = order_data["employer_id"]
        title = order_data["title"]
        description = order_data["description"]
        payment = order_data["payment"]
        start_time = order_data["employer_id"]
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    assert type(
                        employer_id) == int, f"invalid type for employer_id, expected int got {type(employer_id)}"
                    assert type(title) == str, f"invalid type for title, expected str got {type(title)}"
                    assert type(
                        description) == str, f"invalid type for description, expected str got {type(description)}"
                    assert type(payment) == float, f"invalid type for payment, expected float got {type(payment)}"
                    assert type(start_time) == int, f"invalid type for start_time expected int got {type(start_time)}"
                    cursor.execute('SELECT title FROM orders WHERE title = %s', (title,))
                    if cursor.fetchall():
                        return {"status": f"order with title({title}) already exists"}
                    cursor.execute("INSERT INTO orders(employer_id, title, description, payment, start_time)"
                                   "VALUES (%s, %s, %s, %s, %s)",
                                   (employer_id, title, description, payment, start_time))
                    conn.commit()
                    return {"status": "ok"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    # Получение description заказа
    def get_description(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT description FROM orders WHERE title = %s LIMIT 1", (self.title,))
                    out = cursor.fetchone()
                    if out:
                        conn.commit()
                        return {"status": "ok", "out": out[0]}
                    return {"status": "no orders found"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    # Получение id работника
    def get_worker_id(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT worker_id FROM orders WHERE title = %s", (self.title,))
                    out = cursor.fetchone()
                    if out:
                        conn.commit()
                        return {"status": "ok", "out": out[0]}
                    return {"status": "error in query, result = False"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    # Получение payment работника
    def get_payment(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT payment FROM orders WHERE title = %s", (self.title,))
                    out = cursor.fetchone()
                    if out:
                        conn.commit()
                        return {"status": "ok", "out": out[0]}
                    return {"status": "error in query, result = False"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    # Получение start_time работника
    def get_start_time(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT start_time FROM orders WHERE title = %s LIMIT 1", (self.title,))
                    out = cursor.fetchone()
                    if out:
                        conn.commit()
                        return {"status": "ok", "out": out[0]}
                    return {"status": "error in query, result = False"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    # Получение finish_time работника
    def get_finish_time(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT finish_time FROM orders WHERE title = %s LIMIT 1", (self.title,))
                    out = cursor.fetchone()
                    if out:
                        conn.commit()
                        return {"status": "ok", "out": out[0]}
                    return {"status": "order is not finished"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    # Получение mark
    def get_mark(self) -> int or None:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT mark FROM orders WHERE title = %s", (self.title,))
                    out = cursor.fetchone()
                    if out:
                        conn.commit()
                        return {"status": "ok", "out": out[0]}
                    return {"status": "order is not finished"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    # Функция для получения feedback
    def get_feedback(self) -> str or None:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT feedback FROM orders WHERE title = %s LIMIT 1", (self.title,))
                    out = cursor.fetchone()
                    if out:
                        conn.commit()
                        return {"status": "ok", "out": out[0]}
                    return {"status": "order is not finished"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    # Функция для получения cancellation
    def get_cancellation(self) -> str or None:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT cancellation FROM orders WHERE title = %s LIMIT 1", (self.title,))
                    out = cursor.fetchone()
                    if out:
                        conn.commit()
                        return {"status": "ok", "out": out[0]}
                    return {"status": "no cancellation"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    # Функция для получения активных заказов на текущий момент
    @staticmethod
    def get_active_orders(worker_id: int) -> int:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT COUNT(active) WHERE worker_id = %s",
                                   (worker_id,))
                    active_num = cursor.fetchone()[0]
                    return active_num
        except Exception as ex:
            return ex.args[0]
        finally:
            conn.close()

    '''
    Функция для отмены заказа.
    На выход:
    {'status': "ok"}
    {'status': wrong type}
    {'status': unknown error}
    '''

    def set_cancellation(self, cancellation_type: str, finish_time: int) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    assert type(cancellation_type) == str, f"invalid type for cancellation_type, " \
                                                           f"expected str got {type(cancellation_type)}"
                    assert type(finish_time) == int, f"invalid type for finish_time, " \
                                                     f"expected int got {type(finish_time)}"
                    cursor.execute("UPDATE orders SET cancellation = %s WHERE title = %s",
                                   (cancellation_type, self.title))
                    cursor.execute("UPDATE orders SET result = 0 WHERE title = %s",
                                   (self.title,))
                    worker_id = self.get_worker_id()
                    active_orders = self.get_active_orders(worker_id)
                    cursor.execute("UPDATE orders SET active_orders = %s WHERE title = %s",
                                   (active_orders, self.title))
                    cursor.execute("UPDATE orders SET active = %s WHERE title = %s", (False, self.title))
                    cursor.execute("UPDATE orders SET finish_time = %s WHERE title = %s", (finish_time, self.title))
                    return {'status': "ok"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    '''
       Функция для успешного завершения заказа.
       На выход:
       {'status': "ok"}
       {'status': unknown error}
       '''

    def set_done(self, finish_time: int) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    assert type(finish_time) == int, f"invalid type for finish_time, " \
                                                     f"expected int got {type(finish_time)}"
                    cursor.execute("UPDATE orders SET done = %s WHERE title = %s",
                                   (True, self.title))
                    cursor.execute("UPDATE orders SET result = 1 WHERE title = %s",
                                   (self.title,))
                    worker_id = self.get_worker_id()
                    active_orders = self.get_active_orders(worker_id)
                    cursor.execute("UPDATE orders SET active_orders = %s WHERE title = %s",
                                   (active_orders, self.title))
                    cursor.execute("UPDATE orders SET active = %s WHERE title = %s", (False, self.title))
                    cursor.execute("UPDATE orders SET finish_time = %s WHERE title = %s", (finish_time, self.title))
                    return {'status': 'ok'}
        except AssertionError as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    '''
    Функция для получения кортежа (result(0/1), active_orders, payment)
    На выход:
    {"result": "ok", "out": out}
    {'status': wrong type}
    '''

    def get_ml_data(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT result, active_orders  FROM orders WHERE title = %s", (self.title,))
                    result = cursor.fetchone()[0]
                    active_orders = cursor.fetchone()[1]
                    payment = self.get_payment()
                    assert result is not None or active_orders is not None, "order is not finished"
                    out = (result, active_orders, payment)
                    return {"result": "ok", "out": out}
        except AssertionError as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    '''
    Функция для внесения отзыва и оценки
    На выход:
    {'status': 'ok'}
    {'status': wrong type}
    '''

    def add_feedback_and_mark(self, feedback: str, mark: int):
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    assert type(feedback) == str, f"invalid type for feedback, " \
                                                  f"expected str got {type(feedback)}"
                    assert type(mark) == int, f"invalid type for mark, " \
                                              f"expected int got {type(mark)}"
                    cursor.execute("UPDATE orders SET feedback = %s, mark = %s WHERE title = %s",
                                   (feedback, mark, self.title))
                    return {"result": "ok"}
        except AssertionError as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()
