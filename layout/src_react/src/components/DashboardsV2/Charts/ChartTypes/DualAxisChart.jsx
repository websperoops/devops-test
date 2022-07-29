import BaseChart from "./BaseChart";
import DualAxisTheme from '../ChartThemes/DualAxisChartTheme'

class DualAxisChart extends BaseChart {
    get_options() {
        return {
            ...DualAxisTheme,
            credits: {
                enabled: false
            },
            id: this.props.chartId,
            chart: {
                zoomType: 'xy',
                spacingBottom: 25,

            },
            title: {
                text: null
            },
            subtitle: {
                // If subtitle is empty, Highcharts will put the chart in tha place where would be subtitle otherwive. We want to keep the size and place of chart stable in case.
                //    Therfore there is a transparent span for that. (Empty sign or spam would Highchart ignore)
                text: ((this.props.title) || (this.props.title !== undefined)) ? this.props.title : '<span style="opacity:0;">.</span>'
            },
            xAxis: [{ categories: this.props.xAxisTitle, crosshair: true, type: 'datetime' }],
            yAxis: [{
                title: {
                    text: this.props.yAxisTitle,
                    style: {
                        color: '#000000',
                    },
                }

            }, { //secondary axis
                title: {
                    text: this.props.yAxisTitle,
                    style: {
                        color: '#000000',
                    },
                }

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
            legend: {
                layout: 'vertical',
                align: 'left',
                x: 80,
                verticalAlign: 'top',
                y: 55,
                floating: true,
                backgroundColor: 'rgba(255,255,255,0.8)'
            },
        }
    }
}

export default DualAxisChart;
