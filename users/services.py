import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(course):
    """Создание продукта"""

    return stripe.Product.create(name=course.title)


def create_price(product, payment_amount):
    """Создание цены в страйпе"""

    return stripe.Price.create(
        product=product.get('id'),
        currency="rub",
        unit_amount=payment_amount * 100,
    )


def create_stripe_sessions(price):
    """Создание сессии на оплату в страйпе"""

    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')
