
const lineChartTheme = {
    colors: ['#eb8527', '#FFCA3D', '#babbbd', '#2e86ab', '#d20c0f'],
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
        }
    }],
    lang: {
        thousandsSep: ','
    }
};

export default lineChartTheme;