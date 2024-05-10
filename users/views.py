import decimal
import hashlib

from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, HttpResponseRedirect

from django.contrib.auth.decorators import login_required

from django.contrib import auth, messages

from django.urls import reverse

from orders.models import Order, OrderItem
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'title': 'Кафе Олимп - авторизация',
               'form': form
               }
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Поздравляем с успешной регистрацией!!!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm  # возможно тут нужны ()
    context = {'title': 'Кафе Олимп - регистрация',
               'form': form
               }
    return render(request, 'users/registration.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)

    context = {'title': 'Кафе Олимп - профиль',
               'form': form,
               }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def calculate_signature(*args) -> str:
    """Create signature MD5."""
    return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()


def check_signature_result(
    order_number: int,  # invoice number
    received_sum: decimal,  # cost of goods, RU
    received_signature: hex,  # SignatureValue
    password: str  # Merchant password
) -> bool:
    signature = calculate_signature(received_sum, order_number, password)
    #print(signature)
    if signature.lower() == received_signature.lower():
        return True
    return False


def check_success_payment(merchant_password_1: str, number: int, cost: decimal.Decimal, signature: str) -> bool:
    """ Verification of operation parameters ("cashier check") in SuccessURL script.
    :param request: HTTP parameters
    """

    if check_signature_result(number, cost, signature, merchant_password_1):
        return True
    return False


@login_required
def robokassa_paid_yes_or_not(request):
    url = request.META['QUERY_STRING']
    urls = url.split('&')
    urls1 = []
    for i in range(len(urls)):
        urls1.append(urls[i].split('='))
    order = Order.objects.get(id=int(urls1[1][1]))
    #order.is_paid = True
    #order.save()
    return print('Теперь считаюсь оплаченным')


@login_required
def history_of_orders(request):
    url = request.META['QUERY_STRING']
    orders = Order.objects.filter(user=request.user).prefetch_related(
        Prefetch(
            "orderitem_set",
            queryset=OrderItem.objects.select_related("product"),
        )
    ).order_by("-id")
    context = {'title': 'Кафе Олимп - История заказов',
               'orders': orders}
    try:
        if len(url) != 0:
            urls = url.split('&')
            urls1 = []
            for i in range(len(urls)):
                urls1.append(urls[i].split('='))

            check = check_success_payment(merchant_password_1=str('z7Q3USda2lXy2VwOc0Ov'), number=int(urls1[1][1]),
                                          cost=decimal.Decimal(urls1[0][1]), signature=str(urls1[2][1]))
            if check:
                order = Order.objects.get(id=int(urls1[1][1]))
                if not order.is_paid:
                    response_data = {
                        "message": "Заказ оплачен",
                    }
                    try:
                        return JsonResponse(response_data)
                    finally:
                        robokassa_paid_yes_or_not(request)
    finally:
        return render(request, 'users/history_of_orders.html', context)


