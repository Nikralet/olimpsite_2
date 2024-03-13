from django import template

from products.models import Basket, BasketQuerySet

from products.utils import get_user_baskets

register = template.Library()


@register.simple_tag()
def user_baskets(request):
    return get_user_baskets(request)


@register.simple_tag()
def basket_quantity(user):
    baskets = Basket.objects.filter(user=user)
    return baskets.total_quantity()
