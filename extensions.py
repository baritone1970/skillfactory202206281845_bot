import json
import requests
from config import curencies_list


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = curencies_list[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            quote_key = curencies_list[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        if base_key == quote_key:
            raise APIException(f'Одинаковые валюты ({base}) не переводятся!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Ошибка с числом: {amount}!')

        cbr_data = requests.get('https://www.cbr-xml-daily.ru/latest.js')
        currencies = json.loads(cbr_data.content)['rates']
        currencies['RUB'] = 1.0
        base_cost = currencies[base_key]
        quote_cost = currencies[quote_key]
        new_price = amount * (quote_cost / base_cost)
        message = f"Цена {amount} {base} в валюте {quote} : {new_price}"
        return message
