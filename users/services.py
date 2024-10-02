import requests
import stripe
import currencyapicom
from rest_framework import status

from config.settings import STRIPE_API_KEY, CURRENCY_API_KEY, BASE_CUR

stripe.api_key = STRIPE_API_KEY


def convert_base_to_eur(base_price):
    """ Конвертация базовой валюты в ЕВРО """
    # client = currencyapicom.Client(CURRENCY_API_KEY)
    # result = client.latest('EUR', currencies=[BASE_CUR])
    # eur_rate = result['data'][BASE_CUR]['value']
    eur_rate = 7.4533307221
    eur_price = base_price / eur_rate
    return round(eur_price, 2)


def create_stripe_product(name):
    """ Создание элемента ПРОДУКТ в Stripe """
    product = stripe.Product.create(name=name)
    return product


def create_stripe_price(amount, product):
    """ Создание элемента ЦЕНА в Stripe """
    price = stripe.Price.create(
        currency="eur",
        unit_amount_decimal=amount * 100,
        # product_data={"name": product},
        product=product["id"],
    )
    return price


def create_stripe_session(price):
    """ Создание элемента СЕССИЯ в Stripe """
    session = stripe.checkout.Session.create(
        success_url="http://0.0.0.0:7080/",
        line_items=[
            {
                "price": price.get("id"),
                "quantity": 1,
            }
        ],
        mode="payment",
    )
    return session.get('id'), session.get('url')
