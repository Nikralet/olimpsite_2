from django.contrib import admin

from django.db.models import QuerySet

from products.models import ProductCategory, Product, Basket


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'weight', 'number_of_pieces', 'category', 'on_or_off',)
    search_fields = ('name',)
    ordering = ('name',)
    actions = ['on', 'off']
    prepopulated_fields = {"slug": ("name", )}
    list_filter = (
        'category',
        'on_or_off',
    )

    @admin.action(description='Включение всех продуктов')
    def on(self, request, qs: QuerySet):
        qs.update(on_or_off=True)
        
    @admin.action(description='Выключение всех продуктов')
    def off(self, request, qs: QuerySet):
        qs.update(on_or_off=False)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", )
    prepopulated_fields = {"slug": ("name",)}


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp',)
    readonly_fields = ('created_timestamp', )
    extra = 0
