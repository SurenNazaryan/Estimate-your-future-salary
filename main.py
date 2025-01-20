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
    return response['found'], response['items'], response['pages']


def get_vacancies_hh(keyword, pages_count):
    page_number = 0
    vacancies = []
    while page_number < pages_count:
        _, vacancies_on_page, _ = get_page_response_hh(keyword, page_number)
        vacancies.extend(vacancies_on_page)
        page_number += 1
    return vacancies


def get_vacancies_salary_hh(keyword, vacancies):
    vacancies_salaries = []
    for vacancy in vacancies:
        if not vacancy['salary'] or vacancy['salary']['currency'] != 'RUR':
            continue
        min_salary = vacancy['salary']['from']
        max_salary = vacancy['salary']['to']
        if not min_salary:
            min_salary = 0
        if not max_salary:
            max_salary = 0
        average_salary = get_salary(min_salary, max_salary)
        vacancies_salaries.append(average_salary)
    return vacancies_salaries


def get_page_response_sj(keyword, sj_api_token, page_number=0):
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
        'page': page_number,
        'keyword': keyword
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    response = response.json()
    vacancies_count = response['total']
    pages = math.ceil(vacancies_count / vacancies_count_in_page)
    return pages, vacancies_count, response['objects']


def get_vacancies_sj(keyword, sj_api_token, pages_count):
    page = 0
    vacancies = []
    while page < pages_count:
        *_, vacancies_on_page = get_page_response_sj(keyword, sj_api_token, page)
        vacancies.extend(vacancies_on_page)
        page += 1
    return vacancies


def get_vacancies_salary_sj(keyword, sj_api_token, vacancies):
    vacancies_salaries = []
    for vacancy in vacancies:
        min_salary = vacancy['payment_from']
        max_salary = vacancy['payment_to']
        if vacancy['currency'] != 'rub' or not min_salary and not max_salary:
            continue
        average_salary = get_salary(min_salary, max_salary)
        vacancies_salaries.append(average_salary)
    return vacancies_salaries


def get_statistics_table(salaries_statistics, title):
    table_data = [
        ['Язык программирования',
         'Средняя зарплата',
         'Вакансий найдено',
         'Вакансий обработано']
    ]
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
    if min_salary and not max_salary:
        average_salary = int(min_salary * 1.2)
    elif not min_salary and max_salary:
        average_salary = int(max_salary * 0.8)
    else:
        average_salary = int((min_salary + max_salary) / 2)
    return average_salary


def calculate_statistics(language, get_page_response, get_vacancies, get_vacancies_salary, api_token=None):
    keyword = f'Программист {language}'
    if api_token:
        pages_count, vacancies_count, _ = get_page_response(keyword, api_token)
    else:
        vacancies_count, _, pages_count = get_page_response(keyword)
    vacancies = get_vacancies(keyword, api_token, pages_count)
    vacancies_salaries = get_vacancies_salary(keyword, api_token, vacancies)
    vacancies_processed = len(vacancies_salaries)
    average_salary = int(sum(vacancies_salaries) / vacancies_processed) if vacancies_processed else 0
    return {
        "vacancies_found": vacancies_count,
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary
    }


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
        hh_salaries_statistics[language] = calculate_statistics(
            language,
            get_page_response_hh,
            get_vacancies_hh,
            get_vacancies_salary_hh
        )
    for language in languages:
        sj_salaries_statistics[language] = calculate_statistics(
            language,
            get_page_response_sj,
            get_vacancies_sj,
            get_vacancies_salary_sj,
            sj_api_token
        )
    get_statistics_table(hh_salaries_statistics, 'HeadHunter Moscow')
    get_statistics_table(sj_salaries_statistics, 'SuperJob Moscow')