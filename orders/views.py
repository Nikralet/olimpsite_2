from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from orders.templatetags.order_dop import adding_points_for_purchases, viewing_points, basket_total_sum_price, \
    basket_total_sum_price2
from products.models import Basket, BasketQuerySet

from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
from users.models import User


def create_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            print(form.errors)
            try:
                with transaction.atomic():
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
                        print(order.requires_delivery)
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

                        baskets = Basket.objects.filter(user=request.user)
                        point = User.objects.get(id=request.user.id)
                        summing = BasketQuerySet.total_sum_price(baskets)
                        points = viewing_points(request.user)
                        if int(order.deduct_points) == 0:
                            point.loyalty_program = points
                        elif int(order.deduct_points) == 1:
                            if summing >= points:
                                point.loyalty_program = 0

                            elif summing < points:
                                point.loyalty_program = points - summing

                        point.save()

                        # Очистить корзину пользователя после создания заказа
                        basket_items.delete()

                        messages.success(request, 'Заказ оформлен!')

                        return redirect('users:profile')
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
