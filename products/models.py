from django.db import models

from users.models import User


class ProductCategory(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        verbose_name = "Категории продуктов"
        verbose_name_plural = "Категории продуктов"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=0, verbose_name="Цена")  # знаки после запятой и количество цифр в цене
    weight = models.DecimalField(max_digits=8, decimal_places=0, verbose_name="Вес")  # знаки после запятой и количество цифр в весе
    on_or_off = models.BooleanField(default=True, verbose_name="Продаётся")
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.PROTECT, verbose_name="Категория")

    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ("id",)

    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category}'

    def sell_price(self):
        return self.price


class BasketQuerySet(models.QuerySet):
    def total_sum_price(self):
        return sum(basket.sum_price() for basket in self.filter())

    def total_sum_weight(self):
        return sum(basket.sum_weight() for basket in self)

    def total_quantity(self):
        if self:
            return sum(basket.quantity for basket in self)
        return 0


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'

    def sum_price(self):
        sum_price = self.product.price * self.quantity
        return sum_price

    def sum_weight(self):
        return self.product.weight * self.quantity