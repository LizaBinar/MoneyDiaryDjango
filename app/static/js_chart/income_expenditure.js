fetch('/transactions/make_income_expenditure/')
    .then((response) => {
        const data = response.json();

        var speedCanvas = document.getElementById("speedChart");

        Chart.defaults.global.defaultFontSize = 12;

        let dataFirst = {
            label: "Расход",
            data: data.expenditure_data,
            lineTension: 0,
            fill: true,
            borderColor: 'red',
            backgroundColor: 'rgba(253,0,0,0.49)'
        };

        let dataSecond = {
            label: "Доход",
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
    })
