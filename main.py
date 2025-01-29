import requests
import pprint
import math
from terminaltables import AsciiTable
from dotenv import load_dotenv
import os


def get_hh_vacancies(keyword):
    url = 'https://api.hh.ru/vacancies'
    moscow_area = 1
    last_month_period = 30
    page_number = 0
    vacancies = []
    params = {
        'text': keyword,
        'area': moscow_area,
        'period': last_month_period,
        'per_page': 100,
        'page': page_number
        }
    while True:
        response = requests.get(url, params=params)
        response.raise_for_status()
        response = response.json()
        vacancies.extend(response['items'])
        params['page'] += 1
        if params['page'] == response['pages']:
            break
    return vacancies


def get_salaries_hh(vacancies):
    salaries = []
    for vacancy in vacancies:
        if vacancy['salary'] and vacancy['salary']['currency'] == 'RUR':
            min_salary = vacancy['salary']['from']
            max_salary = vacancy['salary']['to']
            average_salary = get_salary(min_salary, max_salary)
            if average_salary:
                salaries.append(average_salary)
    return salaries


def get_sj_vacancies(keyword, sj_api_token):
    url = 'https://api.superjob.ru/2.0/vacancies'
    headers = {
        'X-Api-App-Id': sj_api_token
    }
    moscow_id = 4
    vacancies_count_in_page = 100
    last_month_period = 30
    page_number = 0
    params = {
        'town': moscow_id,
        'count': vacancies_count_in_page,
        'period': last_month_period,
        'page': page_number,
        'keyword': keyword
    }
    vacancies = []
    while True:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        response = response.json()
        vacancies.extend(response['objects'])
        params['page'] += 1
        if not response['more']:
            break
    return vacancies


def get_salaries_sj(vacancies):
    salaries = []
    for vacancy in vacancies:
        if vacancy['currency'] != 'rub':
            continue
        min_salary = vacancy['payment_from']
        max_salary = vacancy['payment_to']
        if not min_salary and not max_salary:
            continue
        average_salary = get_salary(min_salary, max_salary)
        salaries.append(average_salary)
    return salaries


def get_salary(min_salary, max_salary):
    if min_salary and not max_salary:
        average_salary = int(min_salary * 1.2)
    elif not min_salary and max_salary:
        average_salary = int(max_salary * 0.8)
    else:
        average_salary = int((min_salary + max_salary) / 2)
    return average_salary


def get_statistics_table(salaries_statistics, title):
    table_data = [
        ['Язык программирования',
         'Средняя зарплата',
         'Вакансий найдено',
         'Вакансий обработано']
    ]
    for language, stats in salaries_statistics.items():
        table_data.append([
            language,
            stats['average_salary'],
            stats['vacancies_found'],
            stats['vacancies_processed']
            ])
    table = AsciiTable(table_data)
    table.title = title
    return table.table


if __name__ == '__main__':
    load_dotenv()
    sj_api_token = os.environ['SUPERJOB_API_KEY']
    languages = [
        "JavaScript",
        "Java",
        "Python",
        "Ruby",
        "PHP",
        "C++",
        "Objective-C",
        "C#",
        "Shell",
        "Go"
    ]
    hh_salaries_statistics = {}
    sj_salaries_statistics = {}
    for language in languages:
        keyword = f'Программиcт {language}'
        hh_vacancies = get_hh_vacancies(keyword)
        hh_vacancies_count = len(hh_vacancies)
        hh_salaries = get_salaries_hh(hh_vacancies)
        hh_vacancies_processed = len(hh_salaries)
        hh_average_salary = int(
            sum(hh_salaries) / hh_vacancies_processed
        ) if hh_vacancies_processed else 0
        hh_salaries_statistics[language] = {
            "vacancies_found": hh_vacancies_count,
            "vacancies_processed": hh_vacancies_processed,
            "average_salary": hh_average_salary
            }
        sj_vacancies = get_sj_vacancies(keyword, sj_api_token)
        sj_vacancies_count = len(sj_vacancies)
        sj_salaries = get_salaries_sj(sj_vacancies)
        sj_vacancies_processed = len(sj_salaries)
        sj_average_salary = int(
            sum(sj_salaries) / sj_vacancies_processed
        ) if sj_vacancies_processed else 0
        sj_salaries_statistics[language] = {
            "vacancies_found": sj_vacancies_count,
            "vacancies_processed": sj_vacancies_processed,
            "average_salary": sj_average_salary
            }
    print(get_statistics_table(hh_salaries_statistics, 'HeadHunter Moscow'))
    print(get_statistics_table(sj_salaries_statistics, 'SuperJob Moscow'))
