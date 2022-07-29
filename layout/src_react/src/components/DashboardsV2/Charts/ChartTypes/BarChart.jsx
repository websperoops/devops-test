import BaseChart from './BaseChart'
import ColumnChartTheme from '../ChartThemes/ColumnChartTheme'

class BarChart extends BaseChart {
    get_options() {
        return {
            ...ColumnChartTheme,
            credits: {
                enabled: false
            },
            id: this.props.chartId,
            chart: {
                type: 'bar',
                zoomType: 'xy'
            },
            title: {
                text: null
            },
            subtitle: {
                text: ((this.props.title) || (this.props.title !== undefined)) ? this.props.title : '<span style="opacity:0;">.</span>'
            },
            xAxis: {
                type: 'datetime',
                title: {
                    text: this.props.xAxis_title
                }
            },
            yAxis: {
                min: 0,
                title: {
                    text: this.props.yAxis_title,
                    align: 'high'
                },
                labels: {
                    overflow: 'justify',
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr> <td style="color:{series.color};padding:0">{series.name}: </td>' +
                    '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true,
                xDateFormat: '%b %e, %Y'
            },
            plotOptions: {
                series: {
                    stacking: this.props.chartType == 'Stacked_Bar' ? 'normal' : null
                },
                bar: {
                    dataLabels: {
                        formatter: function () {
                            return this.y.toFixed(1)
                        },
                        enabled: true
                    }
                }
            }
        }
    }
}

export default BarChart;