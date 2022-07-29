import Highcharts from 'highcharts'
import BellCurve from 'highcharts/modules/histogram-bellcurve';
import BaseChart from './BaseChart';
import lineChartTheme from '../ChartThemes/LineChartTheme';

BellCurve(Highcharts);

class HistogramChart extends BaseChart {
    _createSeries(chartData) {
        let toGroup = chartData.map(cd => [
            (this.props.groupName ? (this.props.groupName + ': ') : '') + cd[this.props.groupFieldName],
            cd[this.props.xFieldName],
            Number.parseFloat(cd[this.props.yFieldName])
        ])
        let data = [];
        let uniqNames = Array.from(new Set(toGroup.map(d => d[0])));

        uniqNames.map(name => {
            toGroup.filter(cd => cd[0] == name).map(cd => {
                console.log(cd)
                data.push(cd[2])
            })
        })
        return [{
            name: 'Histogram',
            type: 'histogram',
            xAxis: 1,
            yAxis: 1,
            baseSeries: 's1',
            zIndex: -1,
            opacity: '0.8'
        }, {
            name: 'Data',
            type: 'scatter',
            color: 'red',
            data: data,
            id: 's1',
            marker: {
                radius: 1.5
            }
        }]
    }

    get_options() {
        return {
            ...lineChartTheme,
            credits: {
                enabled: false
            },
            id: this.props.chartId,
            title: {
                text: null,
                align: 'center',
            },
            subtitle: {
                // If subtitle is empty, Highcharts will put the chart in tha place where would be subtitle otherwive. We want to keep the size and place of chart stable in  case.
                // Therfore there is a transparent span for that. (Empty sign or spam would Highchart ignore)
                text: ((this.props.title) || (this.props.title !== undefined)) ? this.props.title : '<span style="opacity:0;">.</span>'
            },
            xAxis: [{
                title: {
                    text: this.props.xAxisTitle
                },
                alignTicks: false
            }, {
                title: {
                    text: 'Histogram'
                },
                alignTicks: true,
                opposite: true
            }],

            yAxis: [{
                title: { text: this.props.yAxisTitle }
            }, {
                title: { text: 'Histogram' },
                opposite: true
            }],
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
                histogram: {
                    accessibility: {
                        pointDescriptionFormatter: function (point) {
                            var ix = point.index + 1,
                                x1 = point.x.toFixed(3),
                                x2 = point.x2.toFixed(3),
                                val = point.y;
                            return ix + '. ' + x1 + ' to ' + x2 + ', ' + val + '.';
                        }
                    }
                }
            }
        }
    }
}

export default HistogramChart;
