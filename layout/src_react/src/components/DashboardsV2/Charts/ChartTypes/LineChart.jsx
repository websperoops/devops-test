import BaseChart from './BaseChart';
import lineChartTheme from '../ChartThemes/LineChartTheme';

class LineChart extends BaseChart {
    get_options() {
        return {
            ...lineChartTheme,
            credits: {
                enabled: false
            },
            chart: {
                spacingBottom: 25,
            },
            title: {
                text: null,
                align: 'center',
            },
            xAxis: {
                title: {
                    text: this.props.xAxisTitle,
                },
                type: 'datetime',

            },
            tooltip: {
                headerFormat: '<span style="font-size:12px">{point.key}</span><table>',
                pointFormat: '<tr> <td style="color:{series.color};padding:0">{series.name}: </td>' +
                    '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true,
                xDateFormat: '%b %e, %Y',
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                backgroundColor: 'rgba(255,255,255,0.8)'
            },
            plotOptions: {
                series: {
                    label: {
                        connectorAllowed: false
                    }
                }
            },
            responsive: {
                rules: [{
                    condition: {
                    },
                    chartOptions: {
                        legend: {
                            layout: 'horizontal',
                            align: 'center',
                            verticalAlign: 'bottom'
                        }
                    }
                }]
            },
            id: this.props.chartId,
            subtitle: {
                // If subtitle is empty, Highcharts will put the chart in tha place where would be subtitle otherwive. We want to keep the size and place of chart stable in case.
                // Therfore there is a transparent span for that. (Empty sign or spam would Highchart ignore)
                text: ((this.props.title) || (this.props.title !== undefined)) ? this.props.title : '<span style="opacity:0;">.</span>'
            },
            title: {
                text: null,
                style: {
                    color: '#000000'
                }
            },
            yAxis: {
                labels: {
                    formatter: function () {
                        return this.value.toFixed(0)
                    }
                },
                title: {
                    text: this.props.yAxisTitle,
                    style: {
                        color: '#000000'
                    }
                }
            }
        }
    }
}

export default LineChart;
