import BaseChart from './BaseChart'
import AreaChartTheme from '../ChartThemes/AreaChartTheme';

class AreaSplineChart extends BaseChart {
    get_options() {
        return {
            ...AreaChartTheme,
            credits: {
                enabled: false
            },
            id: this.props.chartId,
            chart: {
                type: 'areaspline',
            },
            colors: ['#eb8527', '#FFCA3D', '#babbbd', '#2e86ab', '#d20c0f'],
            title: {
                align: "left",
                text: null
            },
            subtitle: {
                // If subtitle is empty, Highcharts will put the chart in the place where there would be subtitle otherwise. We want to keep the size and place of chart stable in case.
                //    Therfore there is a transparent span for that. (Empty sign or spam would Highchart ignore)
                text: ((this.props.title) || (this.props.title !== undefined)) ? this.props.title : '<span style="opacity:0;">.</span>'
            },
            xAxis: {
                title: {
                    text: this.props.xAxis_title,
                    style: {
                        color: '#ffffff'
                    }
                },
                type: 'datetime'
            },
            yAxis: {
                title: {
                    text: this.props.yAxis_title,
                    style: {
                        color: '#ffffff'
                    }
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
                areaspline: {
                    fillOpacity: 0.5
                }
            },
            legend: {
                layout: 'vertical',
                align: 'left',
                x: 80,
                verticalAlign: 'top',
                y: 50,
                floating: true,
                backgroundColor: 'rgba(255,255,255,0.8)'
            },
        }
    }
}

export default AreaSplineChart