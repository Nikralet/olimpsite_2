from django.urls import path, include

from products.views import products, basket_add, basket_remove, basket_change, product_details, basket_none


app_name = 'products'

urlpatterns = [
    path('', products, name='index'),
    path('category/<int:category_id>/', products, name='category'),
    path('category/<int:category_id>/page/<int:page_number>/', products, name='paginator'),
    path('page/<int:page_number>/', products, name='paginator'),
    path('baskets/add/', basket_add, name='basket_add'),
    path('baskets/none/', basket_none, name='basket_none'),
    path('baskets/remove/', basket_remove, name='basket_remove'),
    path('baskets/change/', basket_change, name='basket_change'),
    path('details/', product_details, name='product_details'),
]


