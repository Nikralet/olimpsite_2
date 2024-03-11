from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path('create_order/', views.create_order, name='create_order'),
    path('deduction_of_points/', views.deduction_of_points, name='deduction_of_points'),
    path('deduction_of_points_not/', views.deduction_of_points_not, name='deduction_of_points_not'),
]
