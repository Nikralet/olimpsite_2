$(document).ready(function () {
        // Из атрибута href берем ссылку на контроллер django
        var robokassa_paid_yes_or_not = $(this).attr("href");
        var successMessage = $("#jq-notification");
        var data = {
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
        };
        // делаем post запрос через ajax не перезагружая страницу
            $.ajax({
                type: "POST",
                url: robokassa_paid_yes_or_not,
                data: data,
                success: function (data) {
                    // Сообщение
                        console.log(data.message)
                        successMessage.html(data.message);
                        successMessage.fadeIn(500);
                        // Через 1сек убираем сообщение
                        setTimeout(function () {
                        successMessage.fadeOut(2000);
                        }, 3000);

                },

                error: function (data) {
                    console.log("Ошибка");
                },
            });
});