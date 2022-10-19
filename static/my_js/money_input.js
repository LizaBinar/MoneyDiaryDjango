$(function () {
    $('.money_input').maskMoney({thousands: ' ', decimal: '.', allowEmpty: false, allowZero: true});
    let money_value = document.querySelector('.money_input').maskMoney('unmasked');
})

