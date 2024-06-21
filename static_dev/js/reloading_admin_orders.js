$(document).ready(function () {
if (localStorage.length === 1) {
    localStorage.setItem('reload', 'stopped');
};
if (window.location.origin + window.location.pathname === window.location.origin + '/admin/orders/order/') {

    if (localStorage.getItem('reload') === 'stopped') {
            alert('Обновление страницы выключено');
        }
    if (localStorage.getItem('reload') === 'started') {
                setTimeout(function () {
                location.reload(window.location.origin + '/admin/orders/order/')
                }, 60000 * 5);
        }

    myFunction = document.getElementById('reload');

            myFunction.addEventListener('click', function() {
                if (localStorage.getItem('reload') === 'stopped'){
                    localStorage.setItem('reload', 'started');
                }
                else if (localStorage.getItem('reload') === 'started'){
                    localStorage.setItem('reload', 'stopped');
                }
            });
            };
});