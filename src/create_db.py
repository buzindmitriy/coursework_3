from typing import Any

import psycopg2

from config import config


class DBCreate:
    """Класс создает и заполняет таблицы PostgreSQL"""

    def __init__(self, database_name="hh_ru"):
        self.database_name = database_name
        self.__params = config()
        self.__conn = psycopg2.connect(dbname="postgres", **self.__params)

    def create_database(self) -> None:
        """Метод создает базу данных и таблицы"""
        conn = self.__conn
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute(f"DROP DATABASE IF EXISTS {self.database_name}")
            cur.execute(f"CREATE DATABASE {self.database_name}")
        except Exception as e:
            print(f"Произошла ошибка при удалении базы данных: {e}")
        finally:
            cur.close()  # Закрываем курсор после использования
            conn.close()  # Закрываем соединение с базой данных

        conn = psycopg2.connect(dbname=self.database_name, **self.__params)
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE employees (
                        employer_id INT PRIMARY KEY,
                        employer_name VARCHAR(255) NOT NULL,
                        employer_url TEXT NOT NULL
                    )
                """
                )
                cur.execute(
                    """
                    CREATE TABLE vacancies (
                        employer_id INT REFERENCES employees(employer_id),
                        vacancy_name VARCHAR(255) NOT NULL,
                        vacancy_url TEXT PRIMARY KEY,
                        area VARCHAR(255) NOT NULL,
                        salary INT,
                        description TEXT
                    )
                """
                )
                conn.commit()
        except Exception as e:
            print(f"Произошла ошибка при создании таблиц: {e}")
        finally:
            conn.close()

    def save_data_to_database(self, data: list[dict[str, Any]]) -> None:
        """Метод заполняет таблицы данными"""
        if data:
            conn = self.__conn = psycopg2.connect(
                dbname=self.database_name, **self.__params
            )

            with conn.cursor() as cur:
                for employer in data[0]["employers"]:

                    cur.execute(
                        """
                        INSERT INTO employees (employer_id, employer_name, employer_url)
                        VALUES (%s, %s, %s) ON CONFLICT DO NOTHING
                        RETURNING employer_id""",
                        (
                            employer["employer_id"],
                            employer["employer_name"],
                            employer["employer_url"],
                        ),
                    )
                for vacancy in data[0]["vacancies"]:
                    cur.execute(
                        """
                        INSERT INTO vacancies (vacancy_name, employer_id, vacancy_url,
                        area, salary, description)
                        VALUES (%s, %s, %s, %s, %s, %s)""",
                        (
                            vacancy["name"],
                            vacancy["employer_id"],
                            vacancy["url"],
                            vacancy["area"],
                            vacancy["salary"],
                            vacancy["description"],
                        ),
                    )
            conn.commit()
            conn.close()
        else:
            print("Нет данных")
