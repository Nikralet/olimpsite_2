// Когда html документ готов (прорисован)
$(document).ready(function () {
    // берем в переменную элемент разметки с id jq-notification для оповещений от ajax
    var successMessage = $("#jq-notification");
    var warningMessage = $("#jq-notification-warning");

    // Ловим событие клика по кнопке добавить в корзину
    $(document).on("click", ".add-to-basket", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        // Берем элемент счетчика в значке корзины и берем оттуда значение
        var goodsInBasketCount = $("#goods-in-basket-count");
        var basketCount = parseInt(goodsInBasketCount.text() || 0);
        // Получаем id товара из атрибута data-product-id
        var product_id = $(this).data("product-id");

        if (product_id === undefined) {
            var add_to_basket_url = $(this).attr("href");
            var data = {
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            }
            // делаем post запрос через ajax не перезагружая страницу
                $.ajax({
                    type: "POST",
                    url: add_to_basket_url,
                    data: data,
                    success: function (data) {
                        // Сообщение
                        warningMessage.html(data.message);
                        warningMessage.fadeIn(500);
                        // Через 1сек убираем сообщение
                        setTimeout(function () {
                            warningMessage.fadeOut(400);
                        }, 1000);
                    },

                    error: function (data) {
                        console.log("Ошибка при выводе сообщения");
                    },
                });
            }
        else {

        // Из атрибута href берем ссылку на контроллер django
        var add_to_basket_url = $(this).attr("href");
        // Берём значение минимальной массы для товара
        var productMinMass = $(this).data("min-quantity-product");
        // Берём значение общей массы для товара в корзине

        var data = {
            product_id: product_id,
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
        };
        // делаем post запрос через ajax не перезагружая страницу
            $.ajax({
                type: "POST",
                url: add_to_basket_url,
                data: data,
                success: function (data) {
                    // Сообщение
                    successMessage.html(data.message);
                    successMessage.fadeIn(500);
                    // Через 1сек убираем сообщение
                    setTimeout(function () {
                        successMessage.fadeOut(400);
                    }, 1000);
                    var productMass = data.basket_mass / 100
                    console.log(productMass)
                    console.log(productMinMass)
                    // Увеличиваем количество товаров в корзине (отрисовка в шаблоне)
                    if (productMass > productMinMass) {
                        basketCount++;
                        goodsInBasketCount.text(basketCount);
                    }
                    else if (productMass <= productMinMass) {
                        basketCount += productMinMass;
                        goodsInBasketCount.text(basketCount);
                    }

                    // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                    var basketItemsContainer = $("#basket-items-container");
                    basketItemsContainer.html(data.basket_items_html);
                },

                error: function (data) {
                    console.log("Ошибка при добавлении товара в корзину");
                },
            });
        }
    });




    // Ловим собыитие клика по кнопке удалить товар из корзины
    $(document).on("click", ".remove-from-basket", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        // Берем элемент счетчика в значке корзины и берем оттуда значение
        var goodsInBasketCount = $("#goods-in-basket-count");
        var basketCount = parseInt(goodsInBasketCount.text() || 0);

        // Получаем id корзины из атрибута data-basket-id
        var basket_id = $(this).data("basket-id");
        // Из атрибута href берем ссылку на контроллер django
        var remove_from_basket = $(this).attr("href");

        var data = {
            basket_id: basket_id,
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
        };
        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({

            type: "POST",
            url: remove_from_basket,
            data: data,
            success: function (data) {
                // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Уменьшаем количество товаров в корзине (отрисовка)
                basketCount -= data.quantity_deleted;
                if (basketCount <= 0) {
                    basketCount = 0
                }
                goodsInBasketCount.text(basketCount);

                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var basketItemsContainer = $("#basket-items-container");
                basketItemsContainer.html(data.basket_items_html);

            },

            error: function (data) {
                console.log("Ошибка при удалении товара из корзины");
            },
        });
    });


    //
    //
    //
    //
    // Теперь + - количества товара
    // Обработчик события для уменьшения значения
    $(document).on("click", ".decrement", function () {
        // Берем ссылку на контроллер django из атрибута data-basket-change-url
        var url = $(this).data("basket-change-url");
        // Берем id корзины из атрибута data-basket-id
        var basketID = $(this).data("basket-id");
        // Ищем ближайшеий input с количеством
        var $input = $(this).closest('.input-group').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());
        // Берём значение минимальной массы для товара
        var basketMinMass = $(this).data("min-quantity");
        // Если количества больше одного, то только тогда делаем -1
        if (currentValue > basketMinMass) {
            $input.val(currentValue - 1);
            // Запускаем функцию определенную ниже
            // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
            updateBasket(basketID, currentValue - 1, -1, url);
        }
    });

    // Обработчик события для увеличения значения
    $(document).on("click", ".increment", function () {
        // Берем ссылку на контроллер django из атрибута data-basket-change-url
        var url = $(this).data("basket-change-url");
        // Берем id корзины из атрибута data-basket-id
        var basketID = $(this).data("basket-id");
        // Ищем ближайшеий input с количеством
        var $input = $(this).closest('.input-group').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());
        if (currentValue < 50) {
            $input.val(currentValue + 1);

            // Запускаем функцию определенную ниже
            // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
            updateBasket(basketID, currentValue + 1, 1, url);
        }
    });

    function updateBasket(basketID, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                basket_id: basketID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Изменяем количество товаров в корзине
                var goodsInBasketCount = $("#goods-in-basket-count");
                var basketCount = parseInt(goodsInBasketCount.text() || 0);
                basketCount += change;
                goodsInBasketCount.text(basketCount);

                // Меняем содержимое корзины
                var basketItemsContainer = $("#basket-items-container");
                basketItemsContainer.html(data.basket_items_html);

            },
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    };

    // При клике по кнопке описания открываем всплывающее(модальное) окно
    $(document).on("click", "#modalButton", function (e) {
        // Получаем id товара из атрибута data-product-id

        var product_id = $(this).data("product-id");
        var add_to_basket_url = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: add_to_basket_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {

                $('#exampleModal').appendTo('body');
                var productItemsContainer = $("#exampleModal");
                productItemsContainer.html(data.product_items_html);

                $('#exampleModal').modal('show');

            },
            error: function (data) {
                console.log("Ошибка");
            },
        });
    });

    // Собыите клик по кнопке закрыть окна корзины
    $('#exampleModal #button-close').click(function () {
        $('#exampleModal').modal('hide');
    });



    // Обработчик события радиокнопки выбора способа доставки
    $("input[name='requires_delivery']").change(function () {
        var selectedValue = $(this).val();
        // Скрываем или отображаем input ввода адреса доставки
        if (selectedValue === "1") {
            $("#deliveryAddressField").show();
        }
        else {
            $("#deliveryAddressField").hide();
        }
    });

    // Обработчик события радиокнопки списания баллов программы лояльности
    $("input[name='deduct_points']").change(function () {
        var selectedValue = $(this).val();

        // Запускаем пересчёт цены и баллов

        if (selectedValue === "1") {

            var deduction_of_points_url = $(this).attr("href");
            var user = $(this).data("user");
            console.log('nen')
            $.ajax({
            type: "POST",
            url: deduction_of_points_url,
            data: {
                user: user,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                console.log('nen')
                // Сообщение
                console.log(data.message);

                var order_price_and_points = $("#order_price_and_points");
                order_price_and_points.html(data.order_price_and_points_html);

            },
            error: function (data) {
                console.log("Ошибка");
            },
        });
        }
        else {
            console.log('else')
            var deduction_of_points_url = $(this).attr("href");
            var user = $(this).data("user");

            console.log('nin')
            $.ajax({
            type: "POST",
            url: deduction_of_points_url,
            data: {
                user: user,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                console.log('nen')
                // Сообщение
                console.log(data.message);

                var order_price_and_points = $("#order_price_and_points");
                order_price_and_points.html(data.order_price_and_points_html);

            },
            error: function (data) {
                console.log("Ошибка");
            },
        });
        }
    });


    // ограничение на вводимое время в будущем нужно  дополнить + 40 минутами от времени заказа

    function myFunction() {

        const t = new Date().getTime()

        const today = new Date();

        const minDate = (new Date(today.getFullYear(), today.getMonth(), today.getDate() + 1)).toISOString().slice(0, 10);

        const The_day_after_tomorrow = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 3);

        const maxDate = The_day_after_tomorrow.toISOString().slice(0, 10); // .toISOString().slice(0, 10); выдаёт на 1 день меньше изначального числа

        const tomorrowDate = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 2);

        document.querySelectorAll("input[type='date']").forEach((input) => {
            input.setAttribute('max', maxDate);
            input.setAttribute('min', minDate);
        });

        var timeInput = document.getElementById("delivery_time");

        time_deposits = 1 // 1 час или 60 минут

        timeInput_min_standard = '11:00';

        timeInput_max = '21:00';

        timeInput_future = new Date(t + time_deposits * 60 * 60 * 1000).toLocaleTimeString([], { hour: '2-digit', minute: "2-digit" });

//        document.getElementById('delivery_date').value = minDate
        $("input[id='delivery_date']").change(function () {

            var dd = new Date(document.getElementById("delivery_date").value);

            var selectedValue = $(this).val();
            // Скрываем или отображаем input ввода адреса доставки

            if (dd.getDate() === today.getDate()) {

                if (timeInput_future > timeInput_min_standard && timeInput_future < timeInput_max) {

                    timeInput_min = timeInput_future;
                    //console.log('был тут 0');
                    }
                if (timeInput_future < '23:59' && timeInput_future > timeInput_max){

                        document.getElementById('delivery_date').value = tomorrowDate.toISOString().slice(0, 10)
                        timeInput_min = timeInput_min_standard;
                        //console.log('был тут 1');
                        }
                if ( timeInput_future < '11:00' && timeInput_future >= '00:00') {
                        timeInput_min = timeInput_min_standard;
                        //console.log('был тут 2');
                        }

            } else if (dd.getDate() === tomorrowDate.getDate() - 1) {
                timeInput_min = timeInput_min_standard;
            }
            else if (dd.getDate() === The_day_after_tomorrow.getDate() - 1) {
                timeInput_min = timeInput_min_standard;
            }

            timeInput.value = timeInput_min;
            let previousValue = timeInput.value;

            timeInput.onchange = () => {

                if (timeInput.value < timeInput_min || timeInput.value > timeInput_max) {

                    timeInput.value = previousValue;
                }

                previousValue = timeInput.value;
            }
        });
    }

    var start = myFunction();

    time_interval = 10 // 5 - измеряется в  минутах

    var interval = setInterval(function () { myFunction(); }, time_interval * 60 * 1000);
    // тут кончается функция на время заказа, думал будет маленькой, а вышло, это чудо


});

    // При клике по кнопке забыли пароль открываем всплывающее(модальное) окно
    $(document).on("click", "#a_pas", function (e) {
        var forgot_your_password_url = $(this).attr("href_s");
        $.ajax({
            type: "POST",
            url: forgot_your_password_url,
            data: {
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                alert("Забыли пароль? Обратитесь к администратору в кафе «Олимп»! Он поможет вам изменить его.");
            },
            error: function (data) {
                console.log("Ошибка");
            },
        });
    });

