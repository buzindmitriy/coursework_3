from abc import ABC, abstractmethod


class Api(ABC):
    """Абстрактный класс для работы с API по поиску вакансий"""

    @abstractmethod
    def search_query(self) -> None:
        pass


class DataBase(ABC):
    """Абстрактный класс для работы с базой данных PostgreSQL"""

    @abstractmethod
    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """Метод возвращает список всех компаний и количество вакансий у каждой компании."""
        pass

    @abstractmethod
    def get_all_vacancies(self) -> list[tuple]:
        """Метод возвращает список всех вакансий"""
        pass

    @abstractmethod
    def get_avg_salary(self) -> float:
        """Метод возвращает среднюю зарплату по вакансиям"""
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """Метод возвращает список вакансий с заработной платой выше средней по всем вакансиям"""
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, keywords: list[str]) -> None:
        """Метод возвращает список всех вакансий, в названии которых содержатся переданные в метод слова"""
