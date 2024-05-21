import psycopg2


class DBmanager:

    def __init__(self, db_name: str, params: dict):
        self.db_name = db_name
        self.params = params

    async def create_table(self):
        """
        Создание таблицы
        """

        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE tasks (
                        task_id SERIAL PRIMARY KEY,
                        user_id INTEGER,
                        task TEXT,
                        create_date TIMESTAMP
                    )
                """)
        except:
            print("таблица уже существует")
        conn.commit()
        conn.close()

    async def add_task(self, user, task, create_date):
        """
        Вывод списка всех компаний и количество их вакансий
        :return: None
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO tasks (user_id, task, create_date)
                VALUES (%s, %s, %s)
                RETURNING task_id""",
                        (user, task, create_date))
        conn.commit()
        conn.close()

    async def get_task_list(self, user: int):
        """
        Вывод списка задач пользователя
        :param user: tg id пользователя
        :return:
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM tasks
                        WHERE user_id = {user}""")
            data = cur.fetchall()
        conn.commit()
        conn.close()
        return data
