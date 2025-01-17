import requests
import pprint
import math
from terminaltables import AsciiTable
from dotenv import load_dotenv
import os


def get_page_response_hh(keyword, page_number=0):
    url = 'https://api.hh.ru/vacancies'
    moscow_area = 1
    last_month_period = 30
    params = {
        'text': keyword,
        'area': moscow_area,
        'period': last_month_period,
        'per_page': 100,
        'page': page_number
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    url = response.url
    response = response.json()
    return {
        'vacancies_count': response['found'],
        'vacancies_info': response['items'],
        'pages_count': response['pages']
    }


def get_vacancies_hh(keyword):
    pages_count = get_page_response_hh(keyword)['pages_count']
    page_number = 0
    vacancies = []
    while page_number < pages_count:
        vacancies_info = (
            get_page_response_hh(keyword, page_number)['vacancies_info']
        )
        vacancies.extend(vacancies_info)
        page_number += 1
    return vacancies


def get_vacancies_salary_hh(keyword):
    vacancies = get_vacancies_hh(keyword)
    vacancies_salarys = []
    for vacancy in vacancies:
        if not vacancy['salary'] or vacancy['salary']['currency'] != 'RUR':
            continue
        min_salary = vacancy['salary']['from']
        max_salary = vacancy['salary']['to']
        if min_salary is None:
            min_salary = 0
        if max_salary is None:
            max_salary = 0
        average_salary = get_salary(min_salary, max_salary)
        vacancies_salarys.append(average_salary)
    return vacancies_salarys


def get_salaries_statistics_hh(languages):
    salaries_statistics = {}
    for language in languages:
        keyword = f'Программист {language}'
        vacancies_salarys = get_vacancies_salary_hh(keyword)
        vacancies_found = get_page_response_hh(keyword)['vacancies_count']
        vacancies_processed = len(vacancies_salarys)
        if vacancies_processed == 0:
            average_salary = 0
        else:
            average_salary = int(sum(vacancies_salarys) / vacancies_processed)
        salaries_statistics[language] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary
        }
    return salaries_statistics


def get_page_response_sj(keyword, sj_api_token, page=0):
    url = 'https://api.superjob.ru/2.0/vacancies'
    headers = {
        'X-Api-App-Id': sj_api_token
    }
    moscow_id = 4
    vacancies_count_in_page = 100
    last_month_period = 30
    params = {
        'town': moscow_id,
        'count': vacancies_count_in_page,
        'period': last_month_period,
        'page': page,
        'keyword': keyword
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    response = response.json()
    vacancies_count = response['total']
    pages = math.ceil(vacancies_count / vacancies_count_in_page)
    return {
        'pages_count': pages,
        'vacancies_count': vacancies_count,
        'vacancies_info': response['objects']
    }


def get_vacancies_sj(keyword, sj_api_token):
    pages_count = get_page_response_sj(keyword, sj_api_token)['pages_count']
    page = 0
    vacancies = []
    while page < pages_count:
        vacancies_info = (
            get_page_response_sj(keyword, sj_api_token, page)['vacancies_info']
        )
        vacancies.extend(vacancies_info)
        page += 1
    return vacancies


def get_vacancies_salary_sj(keyword, sj_api_token):
    vacancies = get_vacancies_sj(keyword, sj_api_token)
    vacancies_salarys = []
    for vacancy in vacancies:
        min_salary = vacancy['payment_from']
        max_salary = vacancy['payment_to']
        if vacancy['currency'] != 'rub' or min_salary == 0 and max_salary == 0:
            continue
        average_salary = get_salary(min_salary, max_salary)
        vacancies_salarys.append(average_salary)
    return vacancies_salarys


def get_salaries_statistics_sj(languages, sj_api_token):
    salaries_statistics = {}
    for language in languages:
        keyword = f'Программист {language}'
        vacancies_salarys = get_vacancies_salary_sj(keyword, sj_api_token)
        vacancies_found = (
            get_page_response_sj(keyword, sj_api_token)['vacancies_count']
        )
        vacancies_processed = len(vacancies_salarys)
        if vacancies_processed == 0:
            average_salary = 0
        else:
            average_salary = int(sum(vacancies_salarys) / vacancies_processed)
        salaries_statistics[language] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary
        }
    return salaries_statistics


def get_statistics_table(salaries_statistics, title):
    table_data = [
        ['Язык программирования',
         'Средняя зарплата',
         'Вакансий найдено',
         'Вакансий обработано']
    ]  # Заголовки столбцов
    for language, stats in salaries_statistics.items():
        table_data.append(
            [language, 
             stats['average_salary'],
             stats['vacancies_found'],
             stats['vacancies_processed']]
        )
    table = AsciiTable(table_data)
    table.title = title
    print(table.table)


def get_salary(min_salary, max_salary):
    if min_salary != 0 and max_salary == 0:
        average_salary = int(min_salary * 1.2)
    elif min_salary == 0 and max_salary != 0:
        average_salary = int(max_salary * 0.8)
    else:
        average_salary = int((min_salary + max_salary) / 2)
    return average_salary


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
    salaries_statistics_hh = get_salaries_statistics_hh(languages)
    salaries_statistics_sj = get_salaries_statistics_sj(
        languages,
        sj_api_token
    )
    get_statistics_table(salaries_statistics_hh, 'HeadHunter Moscow')
    get_statistics_table(salaries_statistics_sj, 'SuperJob Moscow')
