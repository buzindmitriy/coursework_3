from src.db_manager import DBManager


def user_interface():
    db_manager = DBManager()

    while True:
        print("\n1. Список компаний и количество вакансий")
        print("2. Все вакансии")
        print("3. Средняя зарплата")
        print("4. Вакансии выше средней зарплаты")
        print("5. Вакансии по ключевому слову")
        print("0. Выход")

        choice = input("Выберите опцию: ")

        if choice == '1':
            companies = db_manager.get_companies_and_vacancies_count()
            for company in companies:
                print(f"Компания: {company[0]}, Вакансий: {company[1]}")

        elif choice == '2':
            vacancies = db_manager.get_all_vacancies()
            for vacancy in vacancies:
                print(f"Вакансия: {vacancy[0]}, Зарплата: {vacancy[1]}, Ссылка: {vacancy[2]}, Компания: {vacancy[3]}")

        elif choice == '3':
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата: {avg_salary}")

        elif choice == '4':
            higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
            for vacancy in higher_salary_vacancies:
                print(f"Вакансия: {vacancy[0]}, Зарплата: {vacancy[1]}, Ссылка: {vacancy[2]}, Компания: {vacancy[3]}")

        elif choice == '5':
            keyword = input("Введите ключевое слово: ")
            keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
            for vacancy in keyword_vacancies:
                print(f"Вакансия: {vacancy[0]}, Зарплата: {vacancy[1]}, Ссылка: {vacancy[2]}, Компания: {vacancy[3]}")

        elif choice == '0':
            break

    db_manager.close()


if __name__ == "__main__":
    user_interface()