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
    $('.money_input').maskMoney({thousands: ' ', decimal: '.', allowEmpty: false, allowZero: true});
})



// $(function(){
//     $(".money_input").submit(function() {
//         $('#Total').val($('#Total').maskMoney('unmasked')[0]);
//
// });