from bs4 import BeautifulSoup
from decimal import Decimal


def convert(amount, cur_from, cur_to, date, requests):

    response = requests.get("http://www.cbr.ru/scripts/XML_daily.asp", {"date_req": date})
    soup = BeautifulSoup(response.content, "xml")

    if cur_from == "RUR" or cur_from == "RUB":
        nominal_from = value_from = Decimal(1)
    else:
        nominal_from = from_soup(soup, cur_from, "Nominal")
        value_from = from_soup(soup, cur_from, "Value")

    if cur_to == "RUR" or cur_to == "RUB":
        nominal_to = value_to = Decimal(1)
    else:
        nominal_to = from_soup(soup, cur_to, "Nominal")
        value_to = from_soup(soup, cur_to, "Value")

    from_rub = Decimal(amount) * value_from / nominal_from
    to_rub = Decimal(value_to / nominal_to)

    return Decimal(from_rub/to_rub).quantize(Decimal('1.0000'))


def from_soup(parse, charcode, next_sibling):
    return Decimal(str(parse.find("CharCode", text=charcode).find_next_sibling(next_sibling).string.replace(",", ".")))
