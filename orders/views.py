from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from orders.templatetags.order_dop import viewing_points, basket_total_sum_price, \
    basket_total_sum_price2, adding_points_for_purchases
from products.models import Basket, BasketQuerySet

from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
from users.models import User

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from robokassa.forms import RobokassaForm

import decimal
import hashlib
from urllib import parse
from urllib.parse import urlparse
import threading


def calculate_signature(*args) -> str:
    """Create signature MD5."""
    return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()


def parse_response(request: str) -> dict:
    """
    :param request: Link.
    :return: Dictionary.
    """
    params = {}

    for item in urlparse(request).query.split('&'):
        key, value = item.split('=')
        params[key] = value
    return params


def check_signature_result(
    order_number: int,  # invoice number
    received_sum: decimal,  # cost of goods, RU
    received_signature: hex,  # SignatureValue
    password: str  # Merchant password
) -> bool:
    signature = calculate_signature(received_sum, order_number, password)
    #print(signature)
    if signature.lower() == received_signature.lower():
        return True
    return False


# Формирование URL переадресации пользователя на оплату.

def generate_payment_link(
    merchant_login: str,  # Merchant login
    merchant_password_1: str,  # Merchant password
    cost: decimal,  # Cost of goods, RU
    number: int,  # Invoice number
    description: str,  # Description of the purchase
    is_test = 1,
    robokassa_payment_url = 'https://auth.robokassa.ru/Merchant/Index.aspx',
) -> str:
    """URL for redirection of the customer to the service.
    """
    signature = calculate_signature(
        merchant_login,
        cost,
        number,
        merchant_password_1
    )

    data = {
        'MerchantLogin': merchant_login,
        'OutSum': cost,
        'InvId': number,
        'Description': description,
        'SignatureValue': signature,
        'IsTest': is_test
    }
    return f'{robokassa_payment_url}?{parse.urlencode(data)}'


# Получение уведомления об исполнении операции (ResultURL).

def result_payment(merchant_password_2: str, request: str) -> str:
    """Verification of notification (ResultURL).
    :param request: HTTP parameters.
    """
    param_request = parse_response(request)
    cost = param_request['OutSum']
    number = param_request['InvId']
    signature = param_request['SignatureValue']

    if check_signature_result(number, cost, signature, merchant_password_2):
        return f'OK{param_request["InvId"]}'
    return "bad sign"


# Проверка параметров в скрипте завершения операции (SuccessURL).

def check_success_payment(merchant_password_1: str, request: str) -> bool:
    """ Verification of operation parameters ("cashier check") in SuccessURL script.
    :param request: HTTP parameters
    """
    param_request = parse_response(request)
    cost = param_request['OutSum']
    number = param_request['InvId']
    signature = param_request['SignatureValue']

    if check_signature_result(number, cost, signature, merchant_password_1):
        return True
    return False


@login_required
def create_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            print(form.errors)
            try:
                with (((transaction.atomic()))):
                    user = request.user
                    basket_items = Basket.objects.filter(user=user)

                    if basket_items.exists():
                        # Создать заказ
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get'],
                            deduct_points=form.cleaned_data['deduct_points'],
                            delivery_datetime=datetime.combine(form.cleaned_data['delivery_date'],
                                                               form.cleaned_data['delivery_time'])
                        )
                        # Создать заказанные товары
                        for basket_item in basket_items:
                            product = basket_item.product
                            name = basket_item.product.name
                            price = basket_item.product.sell_price()
                            quantity = basket_item.quantity
                            weight = basket_item.product.weight

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                                weight=weight,
                            )

                            product.save()

                        if int(order.deduct_points) == 0:
                            order.total_cost = basket_total_sum_price(user)
                            order.save()
                        elif int(order.deduct_points) == 1:
                            order.total_cost = basket_total_sum_price2(user)
                            order.save()

                        baskets = Basket.objects.filter(user=user)
                        point = User.objects.get(id=user.id)
                        summing = BasketQuerySet.total_sum_price(baskets)
                        points = viewing_points(user)
                        if int(order.deduct_points) == 0:
                            point.loyalty_program = points
                        elif int(order.deduct_points) == 1:
                            if summing >= points:
                                point.loyalty_program = 0

                            elif summing < points:
                                point.loyalty_program = points - summing

                        point.save()

                        if order.payment_on_get == '0':
                            k = [i.product.name for i in basket_items]
                            text = ''
                            for i in range(len(k)):
                                text += str(k[i]) + ', '
                            text = text[:-2]
                            description = ' Номер заказа: ' + str(order.id) + ';' + ' Время доставки: ' + str(
                                order.delivery_datetime) + ';' + ' Список покупок: ' + text
                            urls = generate_payment_link(merchant_login=str('Cafe-Olimp'),
                                                         merchant_password_1=str('z7Q3USda2lXy2VwOc0Ov'),
                                                         cost=decimal.Decimal(order.total_cost),
                                                         number=int(order.id),
                                                         description=description)
                            return redirect(urls)

                        else:
                            # Очистить корзину пользователя после создания заказа
                            basket_items.delete()

                            messages.success(request, 'Заказ оформлен!')

                            return redirect('users:history_of_orders')
            except ValidationError as e:
                messages.success(request, str(e))
                return redirect('basket:order')
        else:
            print(form.errors)
            print()
            print(form.non_field_errors)
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'phone_number': request.user.phone_number
        }

        form = CreateOrderForm(initial=initial)

    context = {
        'title': 'Оформление заказа',
        'form': form,
        'orders': True,
    }

    return render(request, 'orders/create_order.html', context=context)


@login_required
def deduction_of_points(request):

    new_price = 'new_price'

    order_price_and_points_html = render_to_string("orders/price_weight_points.html",
                                                       {"point": new_price}, request=request)

    response_data = {
        "message": "Баллы учтены",
        "order_price_and_points_html": order_price_and_points_html,
    }
    return JsonResponse(response_data)


@login_required
def deduction_of_points_not(request):

    points = viewing_points(request.user)
    basket_sum_price = basket_total_sum_price(request.user)

    new_price = basket_sum_price - points
    order_price_and_points_html = render_to_string("orders/price_weight_points_not.html",
                                                       {"point": new_price}, request=request)

    response_data = {
        "message": "Учёт баллов убран",
        "order_price_and_points_html": order_price_and_points_html,
    }
    return JsonResponse(response_data)
