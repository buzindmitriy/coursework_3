from typing import Any, Dict, List

from src.employer import Employer
from src.vacancy import Vacancy


def cast_objects_to_dict(
    vacancies: List[Vacancy], employers: List[Employer]
) -> List[Dict[str, Any]]:
    """
    Преобразует списки объектов Vacancy и Employer в единый список словарей.
    """
    result: List[Dict[str, Any]] = [{"vacancies": [], "employers": []}]

    if vacancies:
        result[0]["vacancies"] = [
            {
                "name": vacancy.name,
                "employer_id": vacancy.employer_id,
                "url": vacancy.url,
                "area": vacancy.area,
                "salary": vacancy.salary,
                "description": vacancy.description,
            }
            for vacancy in vacancies
        ]

    if employers:
        result[0]["employers"] = [
            {
                "employer_id": employer.employer_id,
                "employer_name": employer.employer_name,
                "employer_url": employer.employer_url,
            }
            for employer in employers
        ]

    return result
