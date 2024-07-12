import decimal

from django import template

import users.views
from orders.models import *
from products.models import Basket, BasketQuerySet
from users.models import *

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils import timezone

register = template.Library()


@register.simple_tag()
def basket_total_sum_price(user):
    baskets = Basket.objects.filter(user=user)
    summing = BasketQuerySet.total_sum_price(baskets)

    return decimal.Decimal(summing)


@register.simple_tag()
def basket_total_sum_price2(user):

    baskets = Basket.objects.filter(user=user)
    point = User.objects.get(id=user.id)
    points = viewing_points(user)
    basket_sum_price = BasketQuerySet.total_sum_price(baskets)

    if basket_sum_price >= points:
        new_price = basket_sum_price - points
        point.loyalty_program = 0

    elif basket_sum_price < points:
        new_price = 1
        point.loyalty_program = points - basket_sum_price + 1

    return decimal.Decimal(new_price)


@register.simple_tag()
def basket_total_sum_weight(user):
    baskets = Basket.objects.filter(user=user)
    return BasketQuerySet.total_sum_weight(baskets)


@register.simple_tag()
def the_amount_of_the_users_purchases(user):  # функция считывающая общую сумму покупок пользователя
    this_year = timezone.now().year
    this_month = timezone.now().month
    orders = (Order.objects.filter(user=user).filter(is_paid=True)
              .filter(created_timestamp__month=this_month)
              .filter(created_timestamp__year=this_year))

    summing = 0
    for i in range(orders.count()):
        result = OrderItem.objects.filter(order=orders[i]).in_bulk()
        total_price = []
        for j in range(min(result), max(result)+1):
            total_price.append(result[j].price * result[j].quantity)

        summing += sum(total_price)
    return summing


@register.simple_tag()
def order_amount(user):
    orders = Order.objects.filter(user=user).filter(is_paid=True)
    result = OrderItem.objects.filter(order=orders[len(orders)-1]).in_bulk()
    total_price = []
    for j in range(min(result), max(result) + 1):
        total_price.append(result[j].price * result[j].quantity)
    summing = sum(total_price)
    return summing


@register.simple_tag()
def adding_points_for_purchases(user):  # пример функции изменяющей количество баллов
    summ0 = 1000
    summ1 = 5000

    koef1 = 0.02
    koef2 = 0.05

    theamountoftheuserspurchases = the_amount_of_the_users_purchases(user)
    orderamount = order_amount(user)
    point = User.objects.get(id=user.id)
    if theamountoftheuserspurchases > summ1:
        point.loyalty_program += int(orderamount * decimal.Decimal(koef2))
        point.save()
    elif theamountoftheuserspurchases >= summ0:
        point.loyalty_program += int(orderamount * decimal.Decimal(koef1))
        point.save()
    #print(orderamount)
    #print(point.loyalty_program)


@register.simple_tag()
def viewing_points(user):
    point = User.objects.get(id=user.id)
    return point.loyalty_program


@receiver(post_save, sender=Order)
@register.simple_tag()
def change_is_paid(instance, sender, *args, **kwargs):
    if instance.is_paid and not instance.is_add:
        adding_points_for_purchases(instance.user)
        instance.is_add = True
        instance.save()


@register.simple_tag()
def accrual_of_points(user, baskettotalsumprice):
    summ0 = 1000
    summ1 = 5000

    koef1 = 0.02
    koef2 = 0.05

    theamountoftheuserspurchases = the_amount_of_the_users_purchases(user)
    orderamount = baskettotalsumprice
    AccrualOfPoints = 0

    if theamountoftheuserspurchases + orderamount >= summ1:
        AccrualOfPoints = int(orderamount * decimal.Decimal(koef2))

    elif theamountoftheuserspurchases + orderamount >= summ0:
        AccrualOfPoints = int(orderamount * decimal.Decimal(koef1))
    return AccrualOfPoints


@register.simple_tag()
def accrual_of_points1(user):
    return accrual_of_points(user, basket_total_sum_price(user))


@register.simple_tag()
def accrual_of_points2(user):
    return accrual_of_points(user, basket_total_sum_price2(user))

