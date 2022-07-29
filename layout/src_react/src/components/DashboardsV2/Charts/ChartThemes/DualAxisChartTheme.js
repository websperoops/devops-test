const DualAxisChartTheme = {
    colors: ['#e98535', '#dd403a', '#456990', '#dfd6a7', '#36413e', '#698996', '#c17c74', '#247BA0', '#bcac9b', '#ffe0b5'],
    chart: {
        backgroundColor: '#ffffff',
    },
    title: {
        style: {
            color: '#000000',
            fontWeight: 'bold'
        }
    },
    subtitle: {
        style: {
            color: '#000000',
        }
    },
    xAxis: {
        gridLineColor: '#000000',
        lineColor: '#000000',
        minorGridLineColor: '#000000',
        tickColor: '#000000',
        plotLines: [{
            color: '#000000'
        }],
        labels: {
            style: {
                color: '#000000',
            }
        },
        title: {
            style: {
                color: '#000000',
            },
        }
    },
    yAxis: [{
        gridLineColor: '#000000',
        lineColor: '#000000',
        minorGridLineColor: '#000000',
        tickColor: '#000000',
        plotLines: [{
            color: '#000000'
        }],
        labels: {
            style: {
                color: '#000000',
            }
        },
        title: {
            style: {
                color: '#000000',
            },
        }
    }],
    lang: {
        thousandsSep: ','
    }
};


export default DualAxisChartTheme;