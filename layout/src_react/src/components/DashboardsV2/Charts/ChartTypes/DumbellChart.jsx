import BaseChart from './BaseChart'
import Highcharts from 'highcharts'
import DB from 'highcharts/modules/dumbbell'
import LineChartTheme from '../ChartThemes/LineChartTheme'

DB(Highcharts)

class DumbellChart extends BaseChart {
    _createSeries(chartData) { //TODO: Get Correct series format ({name,low,high})
        let toGroup = chartData.map(cd => [
            (this.props.groupName ? (this.props.groupName + ': ') : '') + cd[this.props.groupFieldName],
            cd[this.props.xFieldName],
            Number.parseFloat(cd[this.props.yFieldName])
        ])
        let uniqNames = Array.from(new Set(toGroup.map(d => d[0])));
        let series = uniqNames.map(name => (
            {
                "name": name,
                "data": toGroup.filter(cd => cd[0] == name).map(cd => [cd[0], cd[2], cd[2]]) // [name,low,high]
            }
        )
        )
        return series
    }

    get_options() {
        return {
            ...LineChartTheme,
            credits: {
                enabled: false
            },
            chart: {
                type: 'dumbbell',
                inverted: true
            },
            id: this.props.chartId,
            legend: {
                enabled: false
            },
            tooltip: {
                shared: true,
                useHTML: true,
                xDateFormat: '%b %e, %Y'
            },
            subtitle: {
                // If subtitle is empty, Highcharts will put the chart in tha place where would be subtitle otherwive. We want to keep the size and place of chart stable in case.
                //    Therfore there is a transparent span for that. (Empty sign or spam would Highchart ignore)
                text: ((this.props.title) || (this.props.title !== undefined)) ? this.props.title : '<span style="opacity:0;">.</span>'
            },
            title: {
                text: null
            },
            tooltip: {
                shared: true
            },
            xAxis: {
                type: 'category',
                title: {
                    text: this.props.xAxis_title
                }
            },
            yAxis: {
                title: {
                    text: this.props.yAxis_title,
                }
            },
        }
    }
}

export default DumbellChart;