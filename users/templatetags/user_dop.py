from django import template

from users.models import User

register = template.Library()


@register.simple_tag()
def viewing_points_user(user):
    point = User.objects.get(id=user.id)
    return point.loyalty_program
