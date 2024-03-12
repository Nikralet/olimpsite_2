from django.db import models
from products.models import Product

from users.models import User

from phonenumber_field.modelfields import PhoneNumberField


class OrderitemQueryset(models.QuerySet):

    def total_price(self):
        return sum(basket.sum_price() for basket in self)

    def total_quantity(self):
        if self:
            return sum(basket.quantity for basket in self)
        return 0


class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, blank=True, null=True, verbose_name="Пользователь",
                             default='admin')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
    delivery_datetime = models.DateTimeField(null=True, verbose_name="Дата-время доставки")
    phone_number = PhoneNumberField(blank=True, verbose_name="Номер телефона")
    requires_delivery = models.BooleanField(default=False, verbose_name="Требуется доставка")
    delivery_address = models.TextField(null=True, blank=True, verbose_name="Адрес доставки")
    payment_on_get = models.BooleanField(default=False, verbose_name="Оплата при получении")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    deduct_points = models.BooleanField(default=False, verbose_name="Баллы списаны")
    is_add = models.BooleanField(default=False, verbose_name="Просто функция, не трогать", editable=False)
    status = models.CharField(max_length=50, default='В обработке',
                              choices=[('В обработке', 'В обработке'), ('В пути', 'В пути'), ('Доставлен', 'Доставлен')],
                              verbose_name="Статус заказа")
    total_cost = models.DecimalField(max_digits=8, default=0, decimal_places=0, verbose_name="Суммарная стоимость")

    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ № {self.pk} | Покупатель {self.user.first_name} {self.user.last_name}| Суммарная стоимость: {self.total_cost}"


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(to=Product, on_delete=models.SET_DEFAULT, null=True, verbose_name="Продукт",
                                default=None)
    name = models.CharField(max_length=256, verbose_name="Название")
    price = models.DecimalField(max_digits=8, decimal_places=0, verbose_name="Цена")
    weight = models.DecimalField(max_digits=8, decimal_places=0, verbose_name="Вес")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата продажи")

    class Meta:
        db_table = "order_item"
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"

    objects = OrderitemQueryset.as_manager()

    def products_price(self):
        return self.price * self.quantity

    def products_weight(self):
        return self.weight * self.quantity

    def __str__(self):
        return f"Товар {self.name} | Заказ № {self.order.pk}"

