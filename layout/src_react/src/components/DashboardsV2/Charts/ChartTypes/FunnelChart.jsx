import Highcharts from 'highcharts'
import Funnel from 'highcharts/modules/funnel';
import BaseChart from './BaseChart';
import PieChartTheme from '../ChartThemes/PieChartTheme';

Funnel(Highcharts);

class FunnelChart extends BaseChart {
    get_options() {
        return {
            ...PieChartTheme,
            credits: {
                enabled: false
            },
            chart: {
                type: 'funnel',

            },
            id: this.props.chartId,
            title: {
                text: null,
                align: 'center',
            },
            subtitle: {
                // If subtitle is empty, Highcharts will put the chart in tha place where would be subtitle otherwive. We want to keep the size and place of chart stable in case.
                //    Therfore there is a transparent span for that. (Empty sign or spam would Highchart ignore)
                text: ((this.props.title) || (this.props.title !== undefined)) ? this.props.title : '<span style="opacity:0;">.</span>'
            },
            tooltip: {
                headerFormat: '<span style="font-size:12px">{point.key}</span><table>',
                pointFormat: '<tr> <td style="color:{series.color};padding:0">{series.name}: </td>' +
                    '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            legend: {
                layout: 'vertical',
                align: 'center',
                verticalAlign: 'bottom',
                backgroundColor: 'rgba(255,255,255,0.8)'
            },
            plotOptions: {
                series: {
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b> ({point.y:,.0f})',
                        softConnector: true
                    },
                    center: ['40%', '50%'],
                    neckWidth: '30%',
                    neckHeight: '25%',
                    width: '80%'
                }
            },
            legend: {
                enabled: false
            },
        }
    }
}

export default FunnelChart;
