import BaseChart from './BaseChart';
import ColumnChartTheme from '../ChartThemes/ColumnChartTheme'

class ColumnChart extends BaseChart {
    get_options() {
        return {
            ...ColumnChartTheme,
            credits: {
                enabled: false
            },
            id: this.props.chartId,
            chart: {
                type: 'column',
            },
            colors: ['#e98535', '#dd403a', '#456990', '#dfd6a7', '#36413e', '#698996', '#c17c74', '#247BA0', '#bcac9b', '#ffe0b5'],
            title: {

                text: null
            },
            subtitle: {
                // If subtitle is empty, Highcharts will put the chart in tha place where would be subtitle otherwive. We want to keep the size and place of chart stable in case.
                //    Therfore there is a transparent span for that. (Empty sign or spam would Highchart ignore)
                text: ((this.props.title) || (this.props.title !== undefined)) ? this.props.title : '<span style="opacity:0;">.</span>'
            },
            xAxis: {
                title: {

                    text: this.props.xAxisTitle,
                    style: {
                        color: '#ffffff'
                    }
                },
                type: 'datetime'
            },
            yAxis: {
                min: 0,
                title: {
                    text: this.props.yAxisTitle,
                    style: {
                        color: '#ffffff'
                    }
                },
                stackLabels: {
                    enabled: true,
                    style: {
                        fontWeight: 'bold',
                        color: 'white',
                    },
                    y: -25
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                x: -30,
                verticalAlign: 'top',
                y: 25,
                floating: true,
                backgroundColor: 'rgba(255,255,255,0.8)',
                borderColor: '#CCC',
                borderWidth: 1,
                shadow: false
            },
            tooltip: {
                headerFormat: '<span style="font-size:12px">{point.key}</span><table>',
                pointFormat: '<tr> <td style="color:{series.color};padding:0">{series.name}: </td>' +
                    '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true,
                xDateFormat: '%b %e, %Y'
            },
            plotOptions: {
                column: {
                    dataLabels: {
                        enabled: false, // Turn back on to display labels all the time
                        color: 'white'
                    }
                }
            },

        }
    }
}

export default ColumnChart;
