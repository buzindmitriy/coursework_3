from src.create_db import DBCreate
from src.db_manager import DBManager
from src.employer import Employer
from src.vacancy_search import SearchVacancies
from src.utils import cast_objects_to_dict
from src.vacancy import Vacancy


def main():
    print("=" * 100)
    print("Вас приветствует  программа поиска вакансий с сайта hh.ru")
    print("Получаю вакансии с hh.ru...")
    # получаем вакансии от hh.ru
    vacancies_data = SearchVacancies().search_query()

    print("Сохраняю результаты в базу данных...")
    # создаем базу данных
    create_data_base = DBCreate()
    create_data_base.create_database()
    # создаем список объектов класса Employer
    employers_list = Employer.cast_to_object_list(vacancies_data)
    # создаем список объектов класса Vacancy
    vacancies_list = Vacancy.cast_to_object_list(vacancies_data)
    # сохраняем данные в таблицы базы данных
    vacancies_data = cast_objects_to_dict(vacancies_list, employers_list)
    create_data_base.save_data_to_database(vacancies_data)

    print("Данные сохранены...")
    # создаем объект класса DBManager
    data_base = DBManager()
    employees_list = data_base.get_companies_and_vacancies_count()
    # выводим список компаний и количество открытых вакансий
    print("Вакансии доступны от следующих работодателей:")
    for emp in employees_list:
        print(f"{emp[0]}, открытых вакансий: {emp[1]}")

    user_answer = input(
        "Выберите пункт меню:\n1: Получить список всех доступных вакансий \n"
        "2: Вывести среднюю зарплату по всем вакансиям \n"
        "3: Вывести список вакансий с зарплатой выше средней по всем доступным вакансиям \n"
        "4: Вывести вакансии содержащие ключевое слова в названии \n"
        "5: Завершить работу программы \n"
    )

    while user_answer != "5":
        if user_answer.isdigit():
            if user_answer == "1":
                vacancies_list = data_base.get_all_vacancies()
                for vacancy in vacancies_list:
                    print(f"{vacancy[0]}, {vacancy[1]} Зарплата: {vacancy[2]} Ссылка: {vacancy[3]}")
                user_answer = input(
                    "Выберите пункт меню:\n1: Получить список всех доступных вакансий \n"
                    "2: Вывести среднюю зарплату по всем вакансиям \n"
                    "3: Вывести список вакансий с зарплатой выше средней по всем доступным вакансиям \n"
                    "4: Вывести вакансии содержащие ключевое слова в названии \n"
                    "5: Завершить работу программы \n"
                )
            elif user_answer == "2":
                avg_salary = data_base.get_avg_salary()
                print(f"Средняя зарплата по всем доступным вакансиям: {avg_salary}")
                user_answer = input(
                    "Выберите пункт меню:\n1: Получить список всех доступных вакансий \n"
                    "2: Вывести среднюю зарплату по всем вакансиям \n"
                    "3: Вывести список вакансий с зарплатой выше средней по всем доступным вакансиям \n"
                    "4: Вывести вакансии содержащие ключевое слова в названии \n"
                    "5: Завершить работу программы \n"
                )
            elif user_answer == "3":
                vacancies_list_with_higher_avg_salary = data_base.get_vacancies_with_higher_salary()
                for vacancy in vacancies_list_with_higher_avg_salary:
                    print(f"{vacancy[0]}, {vacancy[1]} Зарплата: {vacancy[2]} Ссылка: {vacancy[3]}")
                user_answer = input(
                    "Выберите пункт меню:\n1: Получить список всех доступных вакансий \n"
                    "2: Вывести среднюю зарплату по всем вакансиям \n"
                    "3: Вывести список вакансий с зарплатой выше средней по всем доступным вакансиям \n"
                    "4: Вывести вакансии содержащие ключевое слова в названии \n"
                    "5: Завершить работу программы \n"
                )
            elif user_answer == "4":
                keywords = input("Введите слова для поиска через пробел").split()
                filtered_vacancies = data_base.get_vacancies_with_keyword(keywords)
                for vacancy in filtered_vacancies:
                    print(f"{vacancy[0]}, {vacancy[1]} Зарплата: {vacancy[2]} Ссылка: {vacancy[3]}")
                user_answer = input(
                    "Выберите пункт меню:\n1: Получить список всех доступных вакансий \n"
                    "2: Вывести среднюю зарплату по всем вакансиям \n"
                    "3: Вывести список вакансий с зарплатой выше средней по всем доступным вакансиям \n"
                    "4: Вывести вакансии содержащие ключевое слова в названии \n"
                    "5: Завершить работу программы \n"
                )
        else:
            print("Не правильный ввод! Введите число!")
            user_answer = input()
    print("Завершение работы!")
    print("=" * 100)


if __name__ == "__main__":
    main()