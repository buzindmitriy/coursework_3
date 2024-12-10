import psycopg2

from config import config
from src.base_class import DataBase


class DBManager(DataBase):
    """Класс для работы с базой данных PostgreSQL"""

    def __init__(self) -> None:
        self.database_name = "hh_ru"
        self.__params = config()
        self.__conn = psycopg2.connect(dbname=self.database_name, **self.__params)

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """Метод возвращает список всех компаний и количество вакансий у каждой компании."""
        with self.__conn as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT employer_name, COUNT(employer_name) FROM vacancies
                            JOIN employees USING(employer_id)
                            GROUP BY employer_name
                            ORDER BY COUNT(employer_name) DESC"""
                )
                result = cur.fetchall()
        return result

    def get_all_vacancies(self) -> list[tuple]:
        """Метод возвращает список всех вакансий"""
        with self.__conn as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT employer_name, vacancy_name, salary, vacancy_url FROM vacancies
                            JOIN employees USING(employer_id)"""
                )
                result = cur.fetchall()
        return result

    def get_avg_salary(self) -> float:
        """Метод возвращает среднюю зарплату по вакансиям"""
        with self.__conn as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT AVG(salary) FROM vacancies")
                result = cur.fetchall()

        return round(float(result[0][0]), 2)

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """Метод возвращает список вакансий с заработной платой выше средней по всем вакансиям"""
        with self.__conn as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT employer_name, vacancy_name, salary, vacancy_url FROM vacancies
                            JOIN employees USING(employer_id)
                            WHERE salary > (SELECT AVG(salary) FROM vacancies)"""
                )
                result = cur.fetchall()
        return result

    def get_vacancies_with_keyword(self, keywords: list[str]) -> list[tuple]:
        """Метод возвращает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        result = []
        with self.__conn as conn:
            with conn.cursor() as cur:
                for word in keywords:
                    cur.execute(
                        f"""SELECT employer_name, vacancy_name, salary, vacancy_url FROM vacancies
                            JOIN employees USING(employer_id)
                            WHERE  vacancy_name ILIKE '%{word}%'"""
                    )
                    result.extend(cur.fetchall())
        return result
