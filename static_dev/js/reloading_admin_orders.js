$(document).ready(function () {
if (localStorage.length === 1) {
    localStorage.setItem('reload', 'stopped');
};
if (localStorage.getItem('reload') === 'stopped') {
        alert('Обновление страницы выключено');
    }
if (localStorage.getItem('reload') === 'started') {
            setTimeout(function () {
            location.reload()
            }, 60000);
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
});