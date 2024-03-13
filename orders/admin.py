from django.contrib import admin

from orders.models import Order, OrderItem

from datetime import datetime

from rangefilter.filters import (
    DateRangeFilterBuilder,
    DateTimeRangeFilterBuilder,
    NumericRangeFilterBuilder,
    DateRangeQuickSelectListFilterBuilder,
)


# admin.site.register(Order)
# admin.site.register(OrderItem)


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
class OrderAdmin(admin.ModelAdmin):
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