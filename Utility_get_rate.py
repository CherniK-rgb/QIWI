from datetime import datetime as dt
import requests
import xml.etree.ElementTree as ET


def iso_format(code):
    c = code.split(" ")
    code_new = c[1]
    iso_code = "./Valute[NumCode='" + str(code_new) + "']/Value"
    return (iso_code)


def formate_date(date):
    # функция для преобразования даты в нужный формат д/м/год
    d = dt.strptime(date, "%Y-%m-%d")
    day = int(d.day)
    if (day < 10) and (day != 0):
        day = str(day)
        day = "0" + day
    month = str(d.month)
    year = str(d.year)
    new_date = str(day + "/" + month + "/" + year)
    return (new_date)


def get_currency_rate(date, code):
    # функция для вывода списка валют
    url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req=' + date
    try:
        r = requests.get(url, timeout=1)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("HTTP error")
        print(errh.args[0])

    exchange_list_node = ET.fromstring(requests.get(url).text).find(code)
    
    if exchange_list_node is not None:
        exchange_list = float(exchange_list_node.text.replace(",", "."))
        print("USD (Доллар США):", exchange_list)
    else:
        print("По введеным данным небыло найдено информации. Проверьте коректность введных данных")


if __name__ == '__main__':
    date = input("Введите желаю дату в формате YYYY-MM-DD: ")
    print(f"Введёная дата: {date}")
    code = "ISO 840"
    code = input("Введите ISO code желаемой страны в формате ISO **** <- code: ")
    print(f"Введеный ISO code: {code}")
    new_data = formate_date(date)
    new_code = iso_format(code)
    get_currency_rate(new_data, new_code)
    