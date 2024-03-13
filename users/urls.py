from django.urls import path

from users.views import login, registration, profile, logout, history_of_orders

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('history_of_orders/', history_of_orders, name='history_of_orders'),
]


