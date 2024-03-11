from django.contrib import admin

# Register your models here.

from products.models import ProductCategory, Product, Basket


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'weight', 'category', 'on_or_off'  )
    search_fields = ('name',)
    ordering = ('name',)
    prepopulated_fields = {"slug": ("name", )}
    list_filter = (
        'category',
        'on_or_off',
    )


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", )
    prepopulated_fields = {"slug": ("name",)}


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp',)
    readonly_fields = ('created_timestamp', )
    extra = 0