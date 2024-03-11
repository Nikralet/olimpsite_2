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