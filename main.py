import requests

main_menu = '''--------------------------
1. Перевод валюты в валюту
2. Узнать курс доллара
3. Узнать курс евро

Выберете действие:\t'''

api_courses = "https://www.cbr-xml-daily.ru/latest.js"
api_valuta_names = "https://www.cbr-xml-daily.ru/daily_json.js"


def to_fixed(number, digits):
    return f"{number:.{digits}f}"


def valuta_convert():
    json_valuta_names = requests.request("GET", api_valuta_names).json()["Valute"]

    valuta_names = [{"key": "RUB", "name": "Российский рубль"}]
    for key, value in json_valuta_names.items():
        valuta_names.append({"key": key, "name": value["Name"]})
    for i in range(len(valuta_names)):
        print(f"{i + 1})\t{valuta_names[i]['name']}")

    index_valuta_begin = input("Веберете из какой валюты будет производиться преобразование:\t")
    if int(index_valuta_begin) < 1 or int(index_valuta_begin) > len(valuta_names):
        print(f"Введите число от 1 до {len(valuta_names)}")
        return
    index_valuta_end = input("Веберете целевую валюту:\t")
    if int(index_valuta_end) < 1 or int(index_valuta_end) > len(valuta_names):
        print(f"Введите число от 1 до {len(valuta_names)}")
        return
    valuta_begin = valuta_names[int(index_valuta_begin) - 1]
    valuta_end = valuta_names[int(index_valuta_end) - 1]

    valuta_courses = requests.request("GET", api_courses).json()["rates"]
    valuta_courses["RUB"] = 1
    sum = float(input(f"Введите сумму в [{valuta_begin['name']}]:\t"))
    multiply = valuta_courses[valuta_end["key"]] / valuta_courses[valuta_begin["key"]]
    result = sum * multiply
    result = to_fixed(result, 2)
    print(f"{sum} в [{valuta_begin['name']}] = {result} в [{valuta_end['name']}]")


def get_course_to_rub(valuta_name):
    response = requests.request("GET", api_courses).json()
    return 1 / response["rates"][valuta_name]


def get_dollar_course():
    course = to_fixed(get_course_to_rub("USD"), 2)
    print(f'1 доллар сша = {course} российских рублей')


def get_euro_course():
    course = to_fixed(get_course_to_rub("EUR"), 2)
    print(f'1 евро = {course} российских рублей')


actions = [
    valuta_convert,
    get_dollar_course,
    get_euro_course
]


def action(choose):
    if int(choose) < 1 or int(choose) > len(actions):
        print(f"Введите число от 1 до {len(actions)}")
        return
    actions[int(choose) - 1]()


while True:
    action(input(main_menu))
