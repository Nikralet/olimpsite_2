from django.contrib import admin

from orders.admin import OrderTabulareAdmin

from users.models import User
from products.admin import BasketAdmin

from django.db.models import QuerySet


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', "first_name", "last_name", 'phone_number', 'loyalty_program')
    search_fields = ("username", "first_name", "last_name", 'loyalty_program')
    actions = ['reset_loyalty_points']

    @admin.action(description='Обнуление баллов программы лояльности')
    def reset_loyalty_points(self, request, qs: QuerySet):
        qs.update(loyalty_program=0)

    inlines = (BasketAdmin, OrderTabulareAdmin)



