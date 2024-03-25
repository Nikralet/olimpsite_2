from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from products.models import ProductCategory, Product, Basket

from products.utils import get_user_baskets

from django.http import JsonResponse

from django.template.loader import render_to_string

from django.core.paginator import Paginator


def index(request):
    if request.user.is_authenticated:
        context = {'title': 'Кафе Олимп',
                   'baskets': Basket.objects.filter(user=request.user),
                   }
    else:
        context = {'title': 'Кафе Олимп'}
    return render(request, 'products/index.html', context)


def we(request):
    if request.user.is_authenticated:
        context = {'title': 'О нас - Кафе Олимп',
                   'baskets': Basket.objects.filter(user=request.user),
                   }
    else:
        context = {'title': 'О нас - Кафе Олимп'}
    return render(request, 'products/we.html', context)


def basket(request):

    context = {'title': 'Корзина - Кафе Олимп',
               'baskets': Basket.objects.filter(user=request.user),
    }
    return render(request, 'products/basket.html', context)


def products(request, category_id=1, page_number=1):
    if category_id:

        category = ProductCategory.objects.get(id=category_id)

        if category == ProductCategory.objects.get(id=1):
            products = Product.objects.all().filter(on_or_off=True)
        else:
            products = Product.objects.filter(category=category).filter(on_or_off=True)

    else:
        products = Product.objects.all().filter(on_or_off=True)

    per_page = 6
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page_number)

    products_value = products.count()

    if request.user.is_authenticated:
        context = {'title': 'Меню - Кафе Олимп',
                   'products': products_paginator,
                   'categoryes': ProductCategory.objects.all(),
                   'baskets': Basket.objects.filter(user=request.user),
                   'products_value': products_value,
                   }
    else:
        context = {'title': 'Меню - Кафе Олимп',
                   'products': products_paginator,
                   'categoryes': ProductCategory.objects.all(),
                   'products_value': products_value,
                   }
    return render(request, 'products/products.html', context)

@login_required
def basket_add(request):

    product_id = request.POST.get("product_id")

    product = Product.objects.get(id=product_id)  # проблема тут с objects т.к. он равен None в models Product
    
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    user_basket = get_user_baskets(request)

    basket_items_html = render_to_string("products/basket_set.html",
                                    {"basket": user_basket}, request=request)

    response_data = {
        "message": "Товар добавлен в корзину",
        "basket_items_html": basket_items_html,
    }

    return JsonResponse(response_data)


def basket_none(request):

    response_data = {
        "message": "Зарегистрируйтесь, чтобы добавлять в корзину",

    }

    return JsonResponse(response_data)


@login_required
def basket_remove(request):

    basket_id = request.POST.get("basket_id")

    basket = Basket.objects.get(id=basket_id)
    quantity = basket.quantity
    basket.delete()

    user_basket = get_user_baskets(request)
    basket_items_html = render_to_string("products/basket_set.html",
                                    {"baskets": user_basket}, request=request)

    response_data = {
        "message": "Товар удалён",
        "basket_items_html": basket_items_html,
        "quantity_deleted": quantity,
    }
    return JsonResponse(response_data)


def basket_change(request):

    basket_id = request.POST.get("basket_id")

    quantity = request.POST.get("quantity")

    basket = Basket.objects.get(id=basket_id)

    basket.quantity = quantity

    basket.save()

    basket = get_user_baskets(request)
    #print(type(basket))
    basket_items_html = render_to_string(
        "products/basket_set.html", {"baskets": basket}, request=request)

    response_data = {
        "message": "Количество изменено",
        "basket_items_html": basket_items_html,
    }

    return JsonResponse(response_data)


def product_details(request):

    product_id = request.POST.get("product_id")

    product = Product.objects.get(id=product_id)

    product_items_html = render_to_string("products/product_details.html",
                                          {'product': product}, request=request)

    response_data = {
        "message": "Открыто описание",
        "product_items_html": product_items_html,
    }

    return JsonResponse(response_data)
