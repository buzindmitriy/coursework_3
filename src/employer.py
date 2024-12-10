from typing import Any, Dict, List


class Employer:
    """Класс для работы с работодателями"""

    __slots__ = ("employer_id", "employer_name", "employer_url")

    def __init__(self, employer_id: int, employer_name: str, employer_url: str) -> None:
        self.employer_id = employer_id
        self.employer_name = employer_name
        self.employer_url = employer_url

    def __str__(self) -> str:
        return f"{self.employer_name}: {self.employer_url}"

    @classmethod
    def cast_to_object_list(cls, data: List[Dict[str, Any]]) -> List["Employer"]:
        """Метод преобразовывает набор данных из JSON в список объектов"""
        employers_list = []
        for item in data:
            employer_info = item.get("employer", {})
            employer_id = employer_info.get("id")
            employer_name = employer_info.get("name", "Не указано")
            employer_url = employer_info.get("url", "Не указано")

            # Проверка на наличие employer_id
            if employer_id is not None:
                employers_list.append(cls(employer_id, employer_name, employer_url))
            else:
                print("Предупреждение: employer_id отсутствует в данных")

        return employers_list
