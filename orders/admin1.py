import os

from django.contrib import admin

from olimpsite.settings import BASE_DIR
from orders.models import Order, OrderItem

from rangefilter.filters import DateRangeFilterBuilder

from django_object_actions import DjangoObjectActions, action


class OrderItemTabulareAdmin(admin.TabularInline):
    model = OrderItem
    fields = "product", "name", "price", "quantity", "weight"
    search_fields = (
        "product",
        "name",
    )
    extra = 0


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = "order", "product", "name", "price", "quantity", "weight"
    search_fields = (
        "order",
        "product",
        "name",
    )


class OrderTabulareAdmin(admin.TabularInline):
    model = Order
    fields = (
        "requires_delivery",
        "status",
        "payment_on_get",
        "is_paid",
        "created_timestamp",
    )

    search_fields = (
        "requires_delivery",
        "payment_on_get",
        "is_paid",
        "created_timestamp",
    )
    readonly_fields = ("created_timestamp",)
    extra = 0


@admin.register(Order)
class OrderAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "phone_number",
        "requires_delivery",
        "status",
        "payment_on_get",
        "is_paid",
        "created_timestamp",
        "delivery_datetime",
    )

    search_fields = (
        "id",
        "phone_number",
    )
    readonly_fields = ("created_timestamp",)
    list_filter = (
        ("created_timestamp", DateRangeFilterBuilder()),
        "requires_delivery",
        "status",
        "payment_on_get",
        "is_paid",


    )
    inlines = (OrderItemTabulareAdmin,)

    class Media:
            js = ('js/reloading_admin_orders.js',)

    @action(label='Вкл/Выкл', description="Кнопка включения/выключения обновления страницы раз в минуту")  # optional
    def publish_this(self, request, obj):
        OB = str(BASE_DIR) + '\static_dev\js/reloading_admin_orders.js'
        OB1 = str(BASE_DIR) + '\static_dev\js/reloading_admin_orders1.js'
        if not os.path.exists(OB):
            os.rename(OB1, OB)
            return
        else:
            os.rename(OB, OB1)
            return
    change_actions = ('publish_this', )
    changelist_actions = ('publish_this', )


