from typing import List, Optional


class Vacancy:
    """Класс для работы с вакансиями"""

    __slots__ = ("name", "employer_id", "url", "area", "salary", "description")

    def __init__(
        self,
        name: str,
        employer_id: int,
        url: str,
        area: Optional[str],
        salary: Optional[int],
        description: Optional[str],
    ) -> None:
        self.name = name
        self.employer_id = employer_id
        self.url = url
        self.area = area if area else "Регион не указан"
        self.salary = salary if salary is not None else 0
        self.description = description if description else "Описание отсутствует"

    def __str__(self) -> str:
        salary_display = "Не указана" if self.salary == 0 else self.salary
        return (
            f"{self.name}: {self.description}, Регион: {self.area}, "
            f"Зарплата: {salary_display}, Ссылка: {self.url}"
        )

    @classmethod
    def cast_to_object_list(cls, vacancies: List[dict]) -> List["Vacancy"]:
        """Метод преобразовывает набор данных из JSON в список объектов"""
        vacancies_list = []
        for item in vacancies:
            name = item.get("name")
            employer_id = item.get("employer", {}).get("id")
            url = item.get("alternate_url")
            area = item.get("area", {}).get("name", "Регион не указан")
            if item["salary"] is None:
                salary = 0
            else:
                salary = item.get("salary").get("from")
            description = item.get("snippet", {}).get(
                "requirement", "Описание отсутствует"
            )
            vacancies_list.append(
                cls(name, employer_id, url, area, salary, description)
            )
        return vacancies_list

    def __lt__(self, other: "Vacancy") -> bool:
        """Метод сравнивает вакансии между собой по зарплате"""
        return self.salary < other.salary
