# Сравниваем вакансии программистов

Проект предназначен для рассчета средней зарплаты по вакансиям для программистов в таких сервисах как [hh.ru](https://hh.ru/) и [superjob.ru](https://www.superjob.ru/) 

## Как установить

### 1. Убедитесь, что Python установлен
Прежде чем запускать файл, убедитесь, что у вас установлен Python. Вы можете проверить это, открыв терминал или командную строку и введя:
`python --version`
или
`python3 --version`.
Если Python установлен, вы увидите версию Python. Если нет, скачайте и установите его с [официального сайта Python](https://www.python.org/downloads/).

### 2. Откройте терминал или командную строку
- **Windows**: Нажмите `Win + R`, введите `cmd` и нажмите `Enter`.
- **macOS**: Найдите "Терминал" через Spotlight (Cmd + Space).
- **Linux**: Откройте терминал через меню приложений или с помощью сочетания клавиш.

### 3. Перейдите в каталог с Python файлами
Используйте команду `cd` (change directory), чтобы перейти в каталог, где находится ваш файл. 
Пример для Windows: 
```
cd C:\Users\ВашеИмя\Documents\project
```
Пример для macOS/Linux: 
```
cd /Users/ВашеИмя/Documents/project
```
### 4. Запустите Python файл
Теперь вы можете запустить файл, используя команду `python` или `python3`, в зависимости от вашей установки. Например, если ваш файл называется `publishing_photo.py`, введите:
```
python main.py
```
или
```
python3 main.py
```
Если ваш файл находится в другом каталоге, вы можете указать полный путь к файлу. Например:
```
python /путь/к/вашему/файлу/main.py
```
### Пример
Если у вас есть файл `main.py`, находящийся в папке `Documents/project`, вы бы сделали следующее:
```
cd ~/Documents/project
```
```
python main.py
```

Или, если вы на Windows:
```
cd C:\Users\ВашеИмя\Documents\project
```
```
python main.py
```

После выполнения этих шагов ваш Python файл должен запуститься, и вы увидите вывод в терминале или командной строке.

## Настройка параметров окружения
В директории проекта создайте файл `.env`, откройте его с помощью блокнота и впишите туда параметр: 
```
SUPERJOB_API_KEY=SUPERJOB_АПИ_КЛЮЧ
```
`SUPERJOB_АПИ_КЛЮЧ` - это ключ для работы с API NASA. Получить этот токен можно на [api.superjob.ru](https://api.superjob.ru/) после регистрации и создания приложения. Ключ выглядит примерно так: `v3.r.134766023.f9e958907f57a85d61a4009d5s17f4f0c6dd63aa.93f096fd1c2e43a9b647fa3df71f52bbcc661e92`

Также необходимо установить сторонние библиотеки, не встроенные в Python и необходимые для функционирования скриптов. Для установки используется PIP. PIP — это утилита командной строки для установки, обновления и удаления сторонних библиотек. Для новых версий Python установщик пакетов Pip устанавливается автоматически вместе с интерпретатором. Запустим командную строку и проверим, что он установлен, для этого выполним команду:
```
pip --version
```
Если pip корректно установлен, то мы увидим в командной строке:
```
pip 24.3.1 from C:\Users\B-ZONE\AppData\Local\Programs\Python\Python313\Lib\site-packages\pip (python 3.13)
```
Что-то пошло не так, если:
```
"pip" не является внутренней или внешней командой, исполняемой программой или пакетным файлом.
```
Скорее всего проблема произошла во время установки Python. Удалите Python и выполните установку заново.

Если pip установлен, то можно переходить к установке библиотек. В проекте используются много сторонних библиотек, чтобы не устанавиливать отдельно каждую, можно использовать команду:
```
pip install -r requirements.txt
```
`requirements.txt` - это текстовый файл в директории проекта, в котором хранятся нужные библиотеки их версии.

Проверить корректность установки можно используя команду:
```
pip freeze
```
В командной строке появится список с установленными библиотеками. Откройте `requirements.txt` и убедитесь, что каждая из указанных в файле библиотек с их версиями присутвует в списке, которую вывела командная строка.

Если все вышеперечисленные рекомендации выполнены, можно переходить к запуску скрипта.

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
