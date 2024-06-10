from django.contrib import admin
from django.contrib.auth.hashers import make_password

from orders.admin import OrderTabulareAdmin

from users.models import User
from products.admin import BasketAdmin
from django.contrib.auth.admin import UserAdmin
from django.db.models import QuerySet
# admin.site.register(User, UserAdmin)


@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = ('username', "first_name", "last_name", 'phone_number', 'loyalty_program')
    search_fields = ("username", "first_name", "last_name", 'loyalty_program')
    actions = ['reset_loyalty_points']
    fieldsets = (
        (("Персонаяльная информация"), {"fields": ("first_name", "last_name", 'phone_number', 'loyalty_program', 'password')}),
        (
            ("Статус"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (("Время"), {"fields": ("last_login", "date_joined")}),
    )

    @admin.action(description='Обнуление баллов программы лояльности')
    def reset_loyalty_points(self, request, qs: QuerySet):
        qs.update(loyalty_program=0)

    inlines = (BasketAdmin, OrderTabulareAdmin)



