$(document).ready(function () {
if (localStorage.length === 1) {
    console.log('тут0')
    localStorage.setItem('reload', 'stopped');
};
console.log(localStorage.getItem('reload'))
console.log(localStorage.length)
if (localStorage.getItem('reload') === 'stopped') {
        alert('Обновление страницы выключено');
        console.log('тут3')
    }
if (localStorage.getItem('reload') === 'started') {
            console.log('тут4')
            setTimeout(function () {
            location.reload()
            }, 6000);
    }

myFunction = document.getElementById('reload');

        myFunction.addEventListener('click', function() {
            console.log('тут')
            if (localStorage.getItem('reload') === 'stopped'){
                localStorage.setItem('reload', 'started');
                console.log('тут1')
            }
            else if (localStorage.getItem('reload') === 'started'){
                localStorage.setItem('reload', 'stopped');
                console.log('тут2')
            }
        });
});