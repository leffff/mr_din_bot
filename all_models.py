import psycopg2
from create_environment import create_environment
from os import getenv

create_environment()

DBNAME = getenv("DBNAME")
USER = getenv("USER")
PASSWORD = getenv("PASSWORD")
PORT = getenv("PORT")
HOST = getenv("HOST")


# Класс для взаимодействия с пользователями
class User:
    '''
    Инициализация объекта класса и проверка есть ли пользователь с данным tg_id в базе данных
    На выход:
    {"status": "ok"}
    {"status": "user not found"}
    {"status": unknown error}
    '''

    def get_from_tg_id(self, tg_id: int) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    assert type(tg_id) == int, f"invalid type for tg_id"
                    cursor.execute("SELECT user_id FROM users WHERE tg_id = %s", (tg_id,))
                    if cursor.fetchone():
                        conn.commit()
                        self.tg_id = tg_id
                        return {"status": "ok"}
                    return {"status": "user not found"}
        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()

    '''
    Добавление нового пользователя
    входной словарь: 
    {"tg_nickname": "str(30)",
    "tg_id: int" 
    "name": "str(30)", 
    "surname": "str(30)", 
    "qualification": "str, str",
    "qualities": "str, str",
    "experience": "int",
    "city": "str(30)"}
    На выход:
     {"status": "ok"}
    {"status": error("invalid type for {e. g. tg_nickname}", unknown)}
    '''

    @staticmethod
    def add_user(user_data: dict):
        tg_nickname = user_data["tg_nickname"]
        tg_id = user_data["tg_id"]
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
                        tg_nickname) == str, "invalid type for tg_nickname"
                    assert type(tg_id) == int, "invalid type for tg_id"
                    assert type(name) == str, "invalid type for name"
                    assert type(surname) == str, "invalid type for surname"
                    assert type(qualification) == str, "invalid type for qualification"
                    assert type(experience) == int, "invalid type for experience"
                    assert type(qualities) == str, "invalid type for qualities"
                    assert type(city) == str, f"invalid type for city"
                    cursor.execute(
                        'INSERT INTO users(tg_nickname, tg_id, name, surname, qualification, experience, qualities, city) '
                        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                        (tg_nickname, tg_id, name, surname, qualification, experience, qualities, city))
                    conn.commit()
                    return {"status": "ok"}
        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()

    '''
    Функция для поиска пользователя по id.
    На выход:
    {"status": "ok", "output": User()}
    {"status": "user not found"}
    {'status': error("invalid type for user_id", unknown)}
    '''

    @staticmethod
    def get_user_by_id(user_id):
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    assert type(user_id) == int, "invalid type for user_id"
                    cursor.execute(f'SELECT tg_id FROM users WHERE user_id = %s', (user_id,))
                    tg_id = cursor.fetchone()
                    if tg_id:
                        conn.commit()
                        user = User()
                        user.get_from_tg_id(tg_id)
                        return {"status": "ok", "output": user}
                    return {"status": "user not found"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    '''
    получение name и surname пользователя
    На выход:
    {'status': "ok", "out": out}
    {"status": "error in query, result = False"}
    {'status': unknown error}
    '''
    def get_name_surname(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT name, surname FROM users WHERE tg_id = %s", (self.tg_id,))
                    out = cursor.fetchone()
                    if out:
                        conn.commit()
                        return {'status': "ok", "out": out}
                    return {"status": "error in query, result = False"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    '''
    получение qualification пользователя
    На выход:
    {'status': "ok", "out": out}
    {"status": "error in query, result = False"}
    {'status': unknown error}
    '''
    def get_qualification(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT qualification FROM users WHERE tg_id = %s", (self.tg_id,))
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
        получение city пользователя
        На выход:
        {'status': "ok", "out": out}
        {"status": "error in query, result = False"}
        {'status': unknown error}
    '''

    def get_city(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT city FROM users WHERE tg_id = %s", (self.tg_id,))
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
    Получение tg_nickname пользователя
    На выход:
    {'status': "ok", "out": out}
    {"status": "error in query, result = False"}
    {'status': unknown error}
    '''
    def get_tg_nickname(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT tg_nickname FROM users WHERE tg_id = %s", (self.tg_id,))
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
    Получение qualities пользователя
    На выход:
    {'status': "ok", "out": out}
    {"status": "error in query, result = False"}
    {'status': unknown error}
    '''
    def get_qualities(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT qualities FROM users WHERE tg_id = %s", (self.tg_id,))
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
    Получение experience пользователя
    На выход:
    {'status': "ok", "out": out}
    {"status": "error in query, result = False"}
    {'status': unknown error}
    '''
    def get_experience(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT experience FROM users WHERE tg_id = %s", (self.tg_id,))
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
    Получение user_id пользователя
    На выход:
    {'status': "ok", "out": out}
    {"status": "error in query, result = False"}
    {'status': unknown error}
    '''
    def get_user_id(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT user_id FROM users WHERE tg_id = %s", (self.tg_id,))
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
    {"status": "ok", "out": tuple(User(), User()...)}
    {"status": "no users in database"}
    {'status': unknown error}
    '''

    @staticmethod
    def get_all_users() -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT tg_id FROM users WHERE qualification != 'работодатель'")
                    out = cursor.fetchall()
                    if out:
                        conn.commit()
                        data = list()
                        for tg_id in out:
                            user = User()
                            user.get_from_tg_id(tg_id)
                            data.append(user)
                        conn.commit()
                        return {"status": "ok", "out": tuple(data)}
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
    {'status': unknown error}
    '''

    def watch_my_works(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    user_id = self.get_user_id()["out"]
                    cursor.execute(
                        "SELECT title FROM orders INNER JOIN users ON worker_id = user_id WHERE user_id = %s",
                        (user_id,))
                    orders = cursor.fetchall()
                    if orders:
                        conn.commit()
                        data = list()
                        for title in orders:
                            order = Order()
                            order.get_by_title(title)
                            data.append(order)
                        return {"status": "ok", "out": tuple(data)}
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
    {'status': unknown error}
    '''

    def watch_my_orders(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    user_id = self.get_user_id()["out"]
                    cursor.execute(
                        "SELECT title FROM orders INNER JOIN users ON employer_id = user_id WHERE user_id = %s",
                        (user_id,))
                    orders = cursor.fetchall()
                    if orders:
                        conn.commit()
                        data = list()
                        for title in orders:
                            order = Order()
                            order.get_by_title(title)
                            data.append(order)
                        return {"status": "ok", "out": tuple(data)}
                    return {"status": "no orders found"}
        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()


class Order:
    '''
    Инициализаци и Проверка title
    На выход:
    {"status": "ok"}
    {"status": "order not found"}
    {"status": error("invalid type for title"), unknown}
    '''

    def get_by_title(self, title: str) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    assert type(title) == str, "invalid type for title"
                    cursor.execute("SELECT order_id FROM orders WHERE title = %s", (title,))
                    if cursor.fetchone():
                        conn.commit()
                        self.title = title
                        return {"status": "ok"}
                    return {"status": "order not found"}
        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()

    '''
    Добавление нового заказа
    Входной словарь:
    {"employer_id": int,
    "title": "str(40),
    "description": "str",
    "payment": float,
    "category": "str(30)"}
    На выход:
    {"status": "ok"}
    {"status": "order with this title already exists"}
    {"status": error("invalid type for {e. g. employer_id}", unknown)}
    '''

    @staticmethod
    def add_order(order_data: dict) -> dict:
        employer_id = order_data["employer_id"]
        title = order_data["title"]
        description = order_data["description"]
        payment = order_data["payment"]
        category = order_data["category"]
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    assert type(employer_id) == int, "invalid type for employer_id"
                    assert type(title) == str, "invalid type for title"
                    assert type(description) == str, "invalid type for description"
                    assert type(payment) == float, "invalid type for payment"
                    assert type(category) == str, "invalid type for category"
                    cursor.execute('SELECT title FROM orders WHERE title = %s', (title,))
                    if cursor.fetchall():
                        return {"status": "order with this title already exists"}
                    cursor.execute("INSERT INTO orders(employer_id, title, description, payment, category)"
                                   "VALUES (%s, %s, %s, %s, %s)",
                                   (employer_id, title, description, payment, category))
                    conn.commit()
                    return {"status": "ok"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    '''
    Получение description заказа
    На выход:
    {"status": "ok", "out": out}
    {"status": "no orders found"}
    {'status': unknown error}
    '''

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

    '''
    Получение id работника
    На выход:
    {"status": "ok", "out": out}
    {"status": "no worker for this order"}
    {'status': unknown error}
    '''

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
                    return {"status": "no worker for this order"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    '''
        Получение payment работника
        На выход:
        {"status": "ok", "out": out}
        {"status": unknown error}
        {"status": "error in query, result = False"}
        '''

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

    '''
        Получение start_time заказа
        На выход:
        {"status": "ok", "out": out}
        {"status": unknown error}
        {"status": "order hasn't started yet"}
        '''

    def get_start_time(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT start_time FROM orders WHERE title = %s", (self.title,))
                    out = cursor.fetchone()
                    if out:
                        conn.commit()
                        return {"status": "ok", "out": out[0]}
                    return {"status": "order hasn't started yet"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    '''
        Получение finish_time заказа
        На выход:
        {"status": "ok", "out": out}
        {"status": unknown error}
        {"status": "order is not finished"}
        '''

    def get_finish_time(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT finish_time FROM orders WHERE title = %s", (self.title,))
                    out = cursor.fetchone()
                    if out:
                        conn.commit()
                        return {"status": "ok", "out": out[0]}
                    return {"status": "order is not finished"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    '''
        Получение mark заказа
        На выход:
        {"status": "ok", "out": out}
        {"status": unknown error}
        {"status": "order is not finished"}
        '''

    def get_mark(self) -> dict:
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

    '''
        Получение feedback заказа
        На выход:
        {"status": "ok", "out": out}
        {"status": unknown error}
        {"status": "order is not finished"}
        '''

    def get_feedback(self) -> dict:
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

    '''
        Получение cancellation заказа
        На выход:
        {"status": "ok", "out": out}
        {"status": unknown error}
        {"status": "no cancellation"}
        '''

    def get_cancellation(self) -> dict:
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
                    conn.commit()
                    return active_num
        except Exception as ex:
            return ex.args[0]
        finally:
            conn.close()

    '''
    Функция для отмены заказа.
    На выход:
    {'status': "ok"}
    {'status': error("invalid type for cancellation_type", "invalid type for finish_time", unknown)}
    '''

    def set_cancellation(self, cancellation_type: str, finish_time: int) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    assert type(cancellation_type) == str, "invalid type for cancellation_type"
                    assert type(finish_time) == int, "invalid type for finish_time"
                    cursor.execute("UPDATE orders SET cancellation = %s WHERE title = %s",
                                   (cancellation_type, self.title))
                    cursor.execute("UPDATE orders SET result = 0 WHERE title = %s",
                                   (self.title,))

                    worker_id = self.get_worker_id()
                    if worker_id["status"] != "ok":
                        return {"status": worker_id["status"]}
                    worker_id = worker_id["out"]
                    active_orders = self.get_active_orders(worker_id)
                    if type(active_orders) != int:
                        return {"status": active_orders}
                    cursor.execute("UPDATE orders SET active_orders = %s WHERE title = %s",
                                   (active_orders, self.title))
                    cursor.execute("UPDATE orders SET active = %s WHERE title = %s", (False, self.title))
                    cursor.execute("UPDATE orders SET finish_time = %s WHERE title = %s", (finish_time, self.title))
                    conn.commit()
                    return {'status': "ok"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    '''
       Функция для успешного завершения заказа.
       На выход:
       {'status': "ok"}
       {'status': error("invalid type for finish_time", unknown)}
       '''

    def set_done(self, finish_time: int) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    assert type(finish_time) == int, "invalid type for finish_time"
                    cursor.execute("UPDATE orders SET done = %s WHERE title = %s",
                                   (True, self.title))
                    cursor.execute("UPDATE orders SET result = 1 WHERE title = %s",
                                   (self.title,))
                    worker_id = self.get_worker_id()
                    if worker_id["status"] != "ok":
                        return {"status": worker_id["status"]}
                    worker_id = worker_id["out"]
                    active_orders = self.get_active_orders(worker_id)
                    if type(active_orders) != int:
                        return {"status": active_orders}
                    cursor.execute("UPDATE orders SET active_orders = %s WHERE title = %s",
                                   (active_orders, self.title))
                    cursor.execute("UPDATE orders SET active = %s WHERE title = %s", (False, self.title))
                    cursor.execute("UPDATE orders SET finish_time = %s WHERE title = %s", (finish_time, self.title))
                    conn.commit()
                    return {'status': 'ok'}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    '''
    Функция для получения кортежа (result(0/1), active_orders, payment)
    На выход:
    {"result": "ok", "out": out}
    {'status': error("order is not finished", unknown)}
    '''

    def get_ml_data(self) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT result, active_orders  FROM orders WHERE title = %s", (self.title,))
                    result = cursor.fetchone()[0]
                    active_orders = cursor.fetchone()[1]
                    payment = self.get_payment()["out"]
                    assert result is None or active_orders is None, "order is not finished"
                    out = (result, active_orders, payment)
                    conn.commit()
                    return {"result": "ok", "out": out}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    '''
    Функция для внесения отзыва и оценки
    На выход:
    {'status': 'ok'}
    {'status': error("invalid type for feedback", "invalid type for mark", unknown)}
    '''

    def add_feedback_and_mark(self, feedback: str, mark: int):
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    assert type(feedback) == str, "invalid type for feedback"
                    assert type(mark) == int, "invalid type for mark"
                    cursor.execute("UPDATE orders SET feedback = %s, mark = %s WHERE title = %s",
                                   (feedback, mark, self.title))
                    conn.commit()
                    return {"result": "ok"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    '''
    Добавление работника и время начала работы в заказ
    На выход:
    {"result": "ok"}
    {'status': error("invalid type for worker_id", "invalid type for start_time", unknown)}
    '''

    def take_task(self, worker_id: int, start_time: int) -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    assert type(worker_id) == int, "invalid type for worker_id"
                    assert type(start_time) == int, "invalid type for start_time"
                    cursor.execute("UPDATE orders SET worker_id = %s, start_time = %s WHERE title = %s",
                                   (worker_id, start_time, self.title))
                    conn.commit()
                    return {"result": "ok"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    '''
        Функция для получения списка классов всех заказов.
        На выход:
        {"status": "ok", "out": tuple(Order(), Order()...)}
        {"status": "no orders in database"}
        {'status': unknown error}
        '''

    @staticmethod
    def get_all_orders() -> dict:
        try:
            with psycopg2.connect(dbname=DBNAME, user=USER,
                                  password=PASSWORD, host=HOST, port=PORT) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT title FROM orders")
                    out = cursor.fetchall()
                    if out:
                        conn.commit()
                        data = list()
                        for title in out:
                            order = Order()
                            order.get_by_title(title)
                            data.append(order)
                        conn.commit()
                        return {"status": "ok", "out": tuple(data)}
                    return {"status": "no orders in database"}
        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()