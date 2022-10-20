"use strict"


function makeIncomeExpenditureChart(id_currency) {
    fetch('/transactions/make_income_expenditure/' + String(id_currency) + '/')
        .then((response) => {
            return response.json();
        })
        .then((data) => {

            let speedCanvas = document.getElementById("speedChart");
            // Chart.defaults.global.defaultFontSize = 12;

            let dataFirst = {
                label: data.title + " Расход",
                data: data.expenditure_data,
                lineTension: 0,
                fill: true,
                borderColor: 'red',
                backgroundColor: 'rgba(253,0,0,0.49)'
            };

            let dataSecond = {
                label: data.title + " Доход",
                data: data.income_data,
                lineTension: 0,
                fill: true,
                backgroundColor: 'rgba(149,200,129,0.51)',
                borderColor: '#2fa800'
            };

            let speedData = {
                labels: data.label,
                datasets: [dataSecond, dataFirst]
            };

            let chartOptions = {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        boxWidth: 80,
                        fontSize: 15,
                        fontColor: 'black'
                    }
                }
            };

            let lineChart = new Chart(speedCanvas, {
                type: 'line',
                data: speedData,
                options: chartOptions
            });
        });
}


Array.from(document.querySelectorAll('.button_income_expenditure'), function (el) {
    el.onclick = function () {
        let id_currency
        id_currency = el.value;
        makeIncomeExpenditureChart(id_currency)
    };
});


function codeAddress() {
    makeIncomeExpenditureChart(1)
}

window.onload = codeAddress;






