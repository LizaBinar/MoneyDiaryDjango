// jQuery('.money_input_').mask('# ##0,00', {
//     reverse: true, placeholder: 'Стартовый баланс'
// });
//
// $(".money_input").numeric({ decimal : ".",  negative : false, scale: 3 });

// $(document).ready(function () {
//     $('.money__input')
//         .inputmask('# ##9', {
//             alias: 'decimal',
//             allowMinus: false,
//             digits: 2,
//             // max: 999.99
//         });
// })

$(function () {
    $('.money_input').maskMoney({thousands: ' ', decimal: '.', allowNegative: true});
    let money_value = document.querySelector('.money_input').maskMoney('unmasked');

    // $(".money_input").submit(function () {
    //     $('.money_input').val($('.money_input').maskMoney('unmasked')[0])
    // });
})



// $(function(){
//     $(".money_input").submit(function() {
//         $('#Total').val($('#Total').maskMoney('unmasked')[0]);
//
// });