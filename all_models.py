import sqlite3
from create_environment import create_environment
from os import getenv

create_environment()

DBNAME = getenv("DBNAME")


# Класс для взаимодействия с пользователями
class User:

    def get_from_tg_id(self, tg_id: int) -> dict:
        """
        Инициализация объекта класса и проверка есть ли пользователь с данным tg_id в базе данных
        На выход:
        {"status": "ok"}
        {"status": "user not found"}
        {"status": unknown error}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                assert type(tg_id) == int, "invalid type for tg_id"
                cursor.execute("SELECT user_id FROM users WHERE tg_id = ?", (tg_id,))
                if cursor.fetchone():
                    conn.commit()
                    self.tg_id = tg_id
                    return {"status": "ok"}
                return {"status": "user not found"}
        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()

    @staticmethod
    def add_user(user_data: dict):
        """
        Добавление нового пользователя
        входной словарь:
        {"tg_nickname": "str(30)",
        "tg_id: int"
        "name": "str(30)",
        "surname": "str(30)",
        "qualification": "str, str",
        "category": "str, str",
        "experience": "int"}
        На выход:
         {"status": "ok"}
        {"status": error("invalid type for {e. g. tg_nickname}", unknown)}
        """

        tg_nickname = user_data["tg_nickname"]
        tg_id = user_data["tg_id"]
        name = user_data["name"]
        surname = user_data["surname"]
        qualification = user_data["qualification"]
        experience = user_data["experience"]
        category = user_data["category"]

        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                assert type(
                    tg_nickname) == str, "invalid type for tg_nickname"
                assert type(tg_id) == int, "invalid type for tg_id"
                assert type(name) == str, "invalid type for name"
                assert type(surname) == str, "invalid type for surname"
                assert type(qualification) == str, "invalid type for qualification"
                assert type(experience) == int, "invalid type for experience"
                assert type(category) == str, "invalid type for category"
                cursor.execute(
                    'INSERT INTO users(tg_nickname, tg_id, name, surname, qualification, experience, category) '
                    'VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (tg_nickname, tg_id, name, surname, qualification, experience, category))
                conn.commit()
                return {"status": "ok"}
        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()

    @staticmethod
    def get_user_by_id(user_id):
        """
        Функция для поиска пользователя по id.
        На выход:
        {"status": "ok", "output": User()}
        {"status": "user not found"}
        {'status': error("invalid type for user_id", unknown)}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                assert type(user_id) == int, "invalid type for user_id"
                cursor.execute(f'SELECT tg_id FROM users WHERE user_id = ?', (user_id,))
                tg_id = cursor.fetchone()[0]
                if tg_id:
                    conn.commit()
                    user = User()
                    user.get_from_tg_id(tg_id)
                    return {"status": "ok", "out": user}
                return {"status": "user not found"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    def get_name(self) -> dict:
        """
        получение name пользователя
        На выход:
        {'status': "ok", "out": out}
        {"status": "error in query, result = False"}
        {'status': unknown error}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM users WHERE tg_id = ?", (self.tg_id,))
                out = cursor.fetchone()[0]
                if out:
                    conn.commit()
                    return {'status': "ok", "out": out}
                return {"status": "error in query, result = False"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    def get_surname(self) -> dict:
        """
        получение surname пользователя
        На выход:
        {'status': "ok", "out": out}
        {"status": "error in query, result = False"}
        {'status': unknown error}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT surname FROM users WHERE tg_id = ?", (self.tg_id,))
                out = cursor.fetchone()[0]
                if out:
                    conn.commit()
                    return {'status': "ok", "out": out}
                return {"status": "error in query, result = False"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    def get_avg_mark(self):
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                user_id = self.get_user_id()["out"]
                cursor.execute("SELECT mark FROM orders WHERE worker_id = ? AND mark IS NOT NULL", (user_id,))
                out = cursor.fetchall()
                if out:
                    conn.commit()
                    avg_mark = round(sum(out) / len(out), 2)
                    return {'status': "ok", "out": avg_mark}
                return {"status": "no marks found", "out": 5}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    def get_qualification(self) -> dict:
        """
        получение qualification пользователя
        На выход:
        {'status': "ok", "out": out}
        {"status": "error in query, result = False"}
        {'status': unknown error}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT qualification FROM users WHERE tg_id = ?", (self.tg_id,))
                out = cursor.fetchone()
                if out:
                    conn.commit()
                    return {"status": "ok", "out": out[0]}
                return {"status": "error in query, result = False"}
        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()

    def get_tg_nickname(self) -> dict:
        """
        Получение tg_nickname пользователя
        На выход:
        {'status': "ok", "out": out}
        {"status": "error in query, result = False"}
        {'status': unknown error}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT tg_nickname FROM users WHERE tg_id = ?", (self.tg_id,))
                out = cursor.fetchone()
                if out:
                    conn.commit()
                    return {"status": "ok", "out": out[0]}
                return {"status": "error in query, result = False"}

        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()

    def get_category(self) -> dict:
        """
        Получение category пользователя
        На выход:
        {'status': "ok", "out": out}
        {"status": "error in query, result = False"}
        {'status': unknown error}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT category FROM users WHERE tg_id = ?", (self.tg_id,))
                out = cursor.fetchone()
                if out:
                    conn.commit()
                    return {"status": "ok", "out": out[0]}
                return {"status": "error in query, result = False"}

        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()

    def get_experience(self) -> dict:
        """
        Получение experience пользователя
        На выход:
        {'status': "ok", "out": out}
        {"status": "error in query, result = False"}
        {'status': unknown error}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT experience FROM users WHERE tg_id = ?", (self.tg_id,))
                out = cursor.fetchone()
                if out:
                    conn.commit()
                    return {"status": "ok", "out": out[0]}
                return {"status": "error in query, result = False"}
        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()

    def get_user_id(self) -> dict:
        """
        Получение user_id пользователя
        На выход:
        {'status': "ok", "out": out}
        {"status": "error in query, result = False"}
        {'status': unknown error}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT user_id FROM users WHERE tg_id = ?", (self.tg_id,))
                out = cursor.fetchone()
                if out:
                    conn.commit()
                    return {"status": "ok", "out": out[0]}
                return {"status": "error in query, result = False"}
        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()

    @staticmethod
    def get_all_users(category) -> dict:
        """
        Функция для получения списка классов всех пользователей.
        На выход:
        {"status": "ok", "out": tuple(tuple(), )}
        {"status": "no workers found"}
        {'status': unknown error}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE qualification != 'работодатель' AND category = ?",
                               (category,))
                out = cursor.fetchall()
                if out:
                    out = list(map(list, out))
                    for worker in out:
                        user = User()
                        tg_id = worker[2]
                        user.get_from_tg_id(tg_id)
                        user_id = user.get_user_id()["out"]
                        cursor.execute("SELECT mark FROM orders WHERE worker_id = ? AND mark IS NOT NULL", (user_id,))
                        out = cursor.fetchall()
                        if out:
                            conn.commit()
                            avg_mark = round(sum(out) / len(out), 2)
                        else:
                            avg_mark = 5
                        worker.append(avg_mark)
                        return {"status": "ok", "out": out}
                return {"status": "no workers found"}
        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()

    def watch_my_works(self) -> dict:
        """
        Функция для просмотра работ человека.
        На выход:
        {"status": "ok", "out": tuple(data)}
        {"status": "no works found"}
        {'status': unknown error}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                user_id = self.get_user_id()["out"]
            cursor.execute(
                "SELECT orders.title FROM orders JOIN users ON worker_id = user_id WHERE user_id = ?",
                (user_id,)
            )
            orders = cursor.fetchall()
            if orders:
                conn.commit()
                data = list()
                for title in orders:
                    order = Order()
                    order.get_by_title(title[0])
                    data.append(order)
                return {"status": "ok", "out": tuple(data)}
            return {"status": "no works found"}

        except Exception as ex:
            return {"status": ex.args[0]}

        finally:
            conn.close()

    def watch_my_orders(self) -> dict:
        """
        Функция для просмотра заказов человека.
        На выход:
        {"status": "ok", "out": tuple(Order(), Order()...)}
        {"status": "no orders found"}
        {'status': unknown error}
        """

        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                user_id = self.get_user_id()["out"]
                cursor.execute(
                    "SELECT orders.title FROM orders JOIN users ON employer_id = user_id WHERE user_id = ?",
                    (user_id,))

                orders = cursor.fetchall()
                if orders:
                    conn.commit()
                    data = list()
                    for title in orders:
                        order = Order()
                        order.get_by_title(title[0])
                        data.append(order)
                    return {"status": "ok", "out": tuple(data)}
                return {"status": "no orders found"}
        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()

    def find_worker_data(self):
        """
        Функция для find_worker
        На выход:
        {"status": "ok", "out": tuple(tuple())}
        {"status": "no orders found"}
        {'status': unknown error}
        """

        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                user_id = self.get_user_id()["out"]
                cursor.execute(
                    "SELECT * FROM orders WHERE employer_id = ? AND worker_id IS NULL",
                    (user_id,))

                orders = cursor.fetchall()
                if orders:
                    conn.commit()
                    return {"status": "ok", "out": orders}
                return {"status": "no orders found"}
        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()


class Order:
    """
    Инициализаци и Проверка title
    На выход:
    {"status": "ok"}
    {"status": "order not found"}
    {"status": error("invalid type for title"), unknown}
    """

    def get_by_title(self, title: str) -> dict:
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                assert type(title) == str, "invalid type for title"
                cursor.execute("SELECT order_id FROM orders WHERE title = ?", (title,))
                if cursor.fetchone():
                    conn.commit()
                    self.title = title
                    return {"status": "ok"}
                return {"status": "order not found"}
        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()

    @staticmethod
    def add_order(order_data: dict) -> dict:
        """
        Добавление нового заказа
        Входной словарь:
        {"employer_id": int,
        "title": "str(40),
        "description": "str",
        "time": int,
        "category": "str(30)",
        "worker_skills": str}
        На выход:
        {"status": "ok"}
        {"status": "order with this title already exists"}
        {"status": error("invalid type for {e. g. employer_id}", unknown)}
        """
        employer_id = order_data["employer_id"]
        title = order_data["title"]
        description = order_data["description"]
        time = order_data["time"]
        category = order_data["category"]
        worker_skills = order_data["worker_skills"]
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                assert type(employer_id) == int, "invalid type for employer_id"
                assert type(title) == str, "invalid type for title"
                assert type(description) == str, "invalid type for description"
                assert type(time) == int, "invalid type for time"
                assert type(category) == str, "invalid type for category"
                assert type(worker_skills) == str, "invalid type for worker_skills"
                cursor.execute('SELECT title FROM orders WHERE title = ?', (title,))
                if cursor.fetchall():
                    return {"status": "order with this title already exists"}
                cursor.execute("INSERT INTO orders(employer_id, title, description, time, category, worker_skills)"
                               "VALUES (?, ?, ?, ?, ?, ?)",
                               (employer_id, title, description, time, category, worker_skills))
                conn.commit()
                return {"status": "ok"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    def get_description(self) -> dict:
        """
        Получение description заказа
        На выход:
        {"status": "ok", "out": out}
        {"status": "error in query, result = False"}
        {'status': unknown error}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT description FROM orders WHERE title = ? ", (self.title,))
                out = cursor.fetchone()[0]
                if out:
                    conn.commit()
                    return {"status": "ok", "out": out}
                return {"status": "error in query, result = False"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    def get_employer_id(self) -> dict:
        """
        Получение id работодателя
        На выход:
        {"status": "ok", "out": out}
        {'status': unknown error}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT employer_id FROM orders WHERE title = ?", (self.title,))
                out = cursor.fetchone()[0]
                if out:
                    conn.commit()
                    return {"status": "ok", "out": out}
                return {"status": "error in query"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    def get_worker_id(self) -> dict:
        """
        Получение id работника
        На выход:
        {"status": "ok", "out": out}
        {"status": "no worker for this order"}
        {'status': unknown error}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT worker_id FROM orders WHERE title = ?", (self.title,))
                out = cursor.fetchone()[0]
                if out:
                    conn.commit()
                    return {"status": "ok", "out": out}
                return {"status": "no worker for this order"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    def get_time(self) -> dict:
        """
        Получение payment работника
        На выход:
        {"status": "ok", "out": out}
        {"status": unknown error}
        {"status": "error in query, result = False"}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT time FROM orders WHERE title = ?", (self.title,))
                out = cursor.fetchone()[0]
                if out:
                    conn.commit()
                    return {"status": "ok", "out": out}
                return {"status": "error in query, result = False"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    def get_category(self) -> dict:
        """
        Получение category заказа
        На выход:
        {"status": "ok", "out": out}
        {"status": unknown error}
        {"status": "error in query, result = False"}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT category FROM orders WHERE title = ?", (self.title,))
                out = cursor.fetchone()[0]
                if out:
                    conn.commit()
                    return {"status": "ok", "out": out}
                return {"status": "error in query, result = False"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    def get_worker_skills(self) -> dict:
        """
        Получение worker_skills заказа
        На выход:
        {"status": "ok", "out": out}
        {"status": unknown error}
        {"status": "error in query, result = False"}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT worker_skills FROM orders WHERE title = ?", (self.title,))
                out = cursor.fetchone()[0]
                if out:
                    conn.commit()
                    return {"status": "ok", "out": out}
                return {"status": "error in query, result = False"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    def get_start_time(self) -> dict:
        """
        Получение start_time заказа
        На выход:
        {"status": "ok", "out": out}
        {"status": unknown error}
        {"status": "order hasn't started yet"}
        """

        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT start_time FROM orders WHERE title = ?", (self.title,))
                out = cursor.fetchone()[0]
                if out:
                    conn.commit()
                    return {"status": "ok", "out": out}
                return {"status": "order hasn't started yet"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    def get_finish_time(self) -> dict:
        """
        Получение finish_time заказа
        На выход:
        {"status": "ok", "out": out}
        {"status": unknown error}
        {"status": "order is not finished"}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT finish_time FROM orders WHERE title = ?", (self.title,))
                out = cursor.fetchone()[0]
                if out:
                    conn.commit()
                    return {"status": "ok", "out": out}
                return {"status": "order is not finished"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    def get_mark(self) -> dict:
        """
        Получение mark заказа
        На выход:
        {"status": "ok", "out": out}
        {"status": unknown error}
        {"status": "order is not finished"}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT mark FROM orders WHERE title = ?", (self.title,))
                out = cursor.fetchone()[0]
                if out:
                    conn.commit()
                    return {"status": "ok", "out": out}
                return {"status": "order is not finished"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    def get_active(self) -> dict:
        """
                Получение active заказа
                На выход:
                {"status": "ok", "out": out}
                {"status": unknown error}
                {"status": "order is not finished"}
                """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT active FROM orders WHERE title = ?", (self.title,))
                out = cursor.fetchone()[0]
                if out:
                    conn.commit()
                    return {"status": "ok", "out": out}
                return {"status": "order is not finished"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    def get_feedback(self) -> dict:
        """
        Получение feedback заказа
        На выход:
        {"status": "ok", "out": out}
        {"status": unknown error}
        {"status": "order is not finished"}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT feedback FROM orders WHERE title = ?", (self.title,))
                out = cursor.fetchone()[0]
                if out:
                    conn.commit()
                    return {"status": "ok", "out": out}
                return {"status": "order is not finished"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    def get_result(self) -> dict:
        """
        Получение result заказа
        На выход:
        {"status": "ok", "out": out}
        {"status": unknown error}
        {"status": "order is not finished"}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT result FROM orders WHERE title = ?", (self.title,))
                out = cursor.fetchone()[0]
                if out is not None:
                    conn.commit()
                    return {"status": "ok", "out": out}
                return {"status": "order is not finished"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    @staticmethod
    def get_active_orders(worker_id: int) -> int:
        # Функция для получения активных заказов на текущий момент
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(active) FROM orders WHERE worker_id = ?",
                               (worker_id,))
                active_num = cursor.fetchone()[0]
                conn.commit()
                return active_num
        except Exception as ex:
            return ex.args[0]
        finally:
            conn.close()

    def set_finished(self, result: int, finish_time: int) -> dict:
        """
        Функция для отмены заказа.
        На выход:
        {'status': "ok"}
        {'status': error("invalid type for result", "invalid type for finish_time", unknown)}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                assert type(result) == int, "invalid type for result"
                assert type(finish_time) == int, "invalid type for finish_time"
                cursor.execute("UPDATE orders SET result = ? WHERE title = ?",
                               (result, self.title))

                worker_id = self.get_worker_id()
                if worker_id["status"] != "ok":
                    return {"status": worker_id["status"]}
                worker_id = worker_id["out"]
                active_orders = self.get_active_orders(worker_id)
                if type(active_orders) != int:
                    return {"status": active_orders}
                cursor.execute("UPDATE orders SET active_orders = ? WHERE title = ?",
                               (active_orders, self.title))
                cursor.execute("UPDATE orders SET active = ? WHERE title = ?", (False, self.title))
                cursor.execute("UPDATE orders SET finish_time = ? WHERE title = ?", (finish_time, self.title))
                conn.commit()
                return {'status': "ok"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    def get_ml_data(self) -> dict:
        """
        Функция для получения кортежа (result(0/1), active_orders, time)
        На выход:
        {"result": "ok", "out": out}
        {'status': error("order is not finished", unknown)}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT result, active_orders  FROM orders WHERE title = ?", (self.title,))
                output = cursor.fetchall()[0]
                result = output[0]
                active_orders = output[1]
                time = self.get_time()["out"]
                assert result is not None, "order is not finished"
                assert active_orders is not None, "order is not finished"
                out = (result, active_orders, time)
                conn.commit()
                return {"result": "ok", "out": out}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    def add_feedback_and_mark(self, feedback: str, mark: int):
        """
        Функция для внесения отзыва и оценки
        На выход:
        {'status': 'ok'}
        {'status': error("invalid type for feedback", "invalid type for mark", unknown)}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                assert type(feedback) == str, "invalid type for feedback"
                assert type(mark) == int, "invalid type for mark"
                cursor.execute("UPDATE orders SET feedback = ?, mark = ? WHERE title = ?",
                               (feedback, mark, self.title))
                conn.commit()
                return {"result": "ok"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    def take_task(self, worker_id: int, start_time: float) -> dict:
        """
        Добавление работника и время начала работы в заказ
        На выход:
        {"result": "ok"}
        {'status': error("invalid type for worker_id", "invalid type for start_time", unknown)}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                cursor = conn.cursor()
                assert type(worker_id) == int, "invalid type for worker_id"
                assert type(start_time) == float, "invalid type for start_time"
                cursor.execute("UPDATE orders SET worker_id = ?, start_time = ?, active = ? WHERE title = ?",
                               (worker_id, start_time, True, self.title))
                conn.commit()
                return {"status": "ok"}
        except Exception as ex:
            return {'status': ex.args[0]}
        finally:
            conn.close()

    @staticmethod
    def get_all_orders(category, employer_id) -> dict:
        """
        Функция для получения списка классов всех заказов.
        На выход:
        {"status": "ok", "out": tuple(Order(), Order()...)}
        {"status": "no orders in database"}
        {'status': unknown error}
        """
        try:
            with sqlite3.connect(DBNAME) as conn:
                assert type(category) == str, "invalid type for category"
                assert type(employer_id) == int, "invalid type for employer_id"
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM orders WHERE category = ? AND employer_id != ?", (category, employer_id))
                out = cursor.fetchall()
                if out:
                    return {"status": "ok", "out": out}
                return {"status": "no orders found"}
        except Exception as ex:
            return {"status": ex.args[0]}
        finally:
            conn.close()
