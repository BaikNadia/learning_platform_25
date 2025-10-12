import stripe
from django.conf import settings
from rest_framework.exceptions import ValidationError

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(course):
    """
    Создаёт продукт в Stripe.
    """
    try:
        product = stripe.Product.create(
            name=course.title,
            description=course.description or "Курс на платформе",
            metadata={"course_id": course.id}
        )
        return product
    except Exception as e:
        raise ValidationError(f"Ошибка при создании продукта в Stripe: {str(e)}")


def create_stripe_price(course):
    """
    Создаёт цену в Stripe (в копейках/центах).
    """
    try:
        unit_amount = int(course.price * 100)  # Конвертируем в минимальные единицы валюты

        if unit_amount < 5000:  # Минимум ~$50 RUB (эквивалент $0.50 USD)
            raise ValidationError("Цена слишком низкая. Минимальная сумма — эквивалент $0.50.")

        price = stripe.Price.create(
            product_data={"name": course.title},
            unit_amount=unit_amount,
            currency="rub",  # можно поменять на 'usd'
            metadata={"course_id": course.id}
        )
        return price
    except Exception as e:
        raise ValidationError(f"Ошибка при создании цены в Stripe: {str(e)}")


def create_checkout_session(course, user_email):
    """
    Создаёт сессию оплаты в Stripe.
    Возвращает URL для оплаты.
    """
    try:
        # 1. Создаём Product, если ещё не существует
        product = create_stripe_product(course)

        # 2. Создаём Price
        price = create_stripe_price(course)

        # 3. Создаём Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price.id,
                'quantity': 1,
            }],
            mode='payment',
            success_url=settings.SITE_URL + '/success/',
            cancel_url=settings.SITE_URL + '/cancel/',
            client_reference_id=str(course.id),
            customer_email=user_email,
        )

        return {
            "checkout_url": session.url,
            "session_id": session.id,
            "price_id": price.id,
            "product_id": product.id,
        }

    except Exception as e:
        raise ValidationError(f"Ошибка при создании сессии оплаты: {str(e)}")
