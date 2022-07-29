import BaseChart from './BaseChart'
import Highcharts from 'highcharts'
import HM from 'highcharts/modules/heatmap'
import lineChartTheme from '../ChartThemes/LineChartTheme'

HM(Highcharts)

class HeatMapChart extends BaseChart {

    constructor(props) {
        super(props);
        this.get_options = this.get_options.bind(this)
    }

    _createSeries(chartData) {
        let toGroup = chartData.map(cd => [
            cd[this.props.groupFieldName],
            cd[this.props.xFieldName],
            Number.parseFloat(cd[this.props.yFieldName])
        ])
        let uniqNames = Array.from(new Set(toGroup.map(d => d[0])));
        let series = uniqNames.map(name => ({
                "data": toGroup.filter(cd => cd[0] == name).map(cd => {
                    // console.log(cd)
                    return { //TODO: configure this correctly.
                        x: new Date(cd[1]).getHours() + 1,
                        y: new Date(cd[1]).getDay(),
                        value: Number.parseFloat(cd[0]) ? Number.parseFloat(cd[0]) : 0
                    }
                }),
                dataLabels: {
                    enabled: true,
                    color: '#000000'
                },
            }
        )
        )
        return series
    }

    get_options(props = this.props) {
        return {
            ...lineChartTheme,
            credits: {
                enabled: false
            },
            chart: {
                type: 'heatmap',
            },
            id: this.props.chartId,
            title: {
                text: null
            },
            subtitle: {
                text: ((this.props.title) || (this.props.title !== undefined)) ? this.props.title : '<span style="opacity:0;">.</span>'
            },
            yAxis: {
                title: {
                    text: null
                },
                categories: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
                reversed: true
            },
            xAxis: {
                opposite: true,
                title: {
                    text: null
                },
                categories: ['11PM', '12 AM', '1 AM', '2 AM', '3 AM ', '4 AM', '5 AM', '6 AM', '7 AM', '8 AM', '9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM', '9 PM', '10 PM', '11 PM'],

                // type: 'datetime'
            },
            tooltip: {
                headerFormat: '<span style="font-size:12px">{point.key}</span><table>',
                // pointFormat: '<tr> <td style="color:{series.color};padding:0;">{series.name}: </td>' + '<br>' +
                //     '<td style="padding:0"><b>{point.value}</b></td></tr>',
                pointFormat: `<div class="d-flex flex-column"> <p style="color:{series.color}; padding:0">${props.groupName}</p>
                <p style="margin:0; padding:0;text-align:center;margin-top:-10px">${props.chartName.toLowerCase().includes('aov') ? '${point.value}' : '{point.value}'}</p> </div>`,
                footerFormat: '</table>',
                shared: true,
                useHTML: true,
                xDateFormat: '%b %e, %Y',
                formatter: props.chartName.includes('AOV') || props.chartName.includes('Sales') ? function () { return `$${this.point.value}` } : function () { return this.point.value },
            },
            colorAxis: {
                min: 0,
                maxColor: '#eb8527',
                minColor: '#fff'
            },
            plotOptions: {
                heatmap: {
                    dataLabels: {
                        formatter: props.chartName.includes('AOV') || props.chartName.includes('Sales') ? function () { return `$${this.point.value}` } : function () { return this.point.value },
                        enabled: true
                    }
                }
            }
        }
    }
}

export default HeatMapChart;