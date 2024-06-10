from django.urls import path

from users.views import login, registration, profile, logout, history_of_orders, robokassa_paid_yes_or_not
from django.contrib.auth import views as auth_views
app_name = 'users'

urlpatterns = [
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('history_of_orders/', history_of_orders, name='history_of_orders'),
    path('history_of_orders/robokassa_paid_yes_or_not/', robokassa_paid_yes_or_not, name='robokassa_paid_yes_or_not'),
]


