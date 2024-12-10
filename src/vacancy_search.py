from typing import Any, List

import requests

from src.base_class import Api


class SearchVacancies(Api):
    """Класс для поиска вакансий с помощью API"""

    def __init__(self) -> None:
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {
            "employer_id": [
                "3096092",
                "1579449",
                "856498",
                "633069",
                "3025983",
                "4480129",
                "1918903",
                "5971349",
                "6093775",
                "1296244",
            ],
            "page": 0,
            "per_page": 100,
        }
        self.__vacancies: List[Any] = []

    def get_total_pages(self) -> int:
        """Получает общее количество страниц"""
        response = self._make_request()
        return response.json()["pages"]

    def _make_request(self) -> requests.Response:
        """Создает запрос к API."""
        try:
            response = requests.get(
                self.__url, headers=self.__headers, params=self.__params
            )
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Ошибка запроса: {e}")
            raise

    def search_query(self, max_pages: int = None) -> List[Any]:
        """Выполняет поисковый запрос и возвращает все вакансии"""
        total_pages = self.get_total_pages()
        max_page = min(total_pages, max_pages) if max_pages else total_pages

        while self.__params["page"] < max_page:
            response = self._make_request()
            vacancies = response.json()["items"]
            self.__vacancies.extend(vacancies)
            self.__params["page"] += 1

        return self.__vacancies

    def get_vacancies(self, page: int = 0) -> List[Any]:
        """Получает вакансии для определенной страницы."""
        self.__params["page"] = page
        return self.search_query(page + 1)

    def clear_vacancies(self) -> None:
        """Очищает список вакансий."""
        self.__vacancies.clear()
