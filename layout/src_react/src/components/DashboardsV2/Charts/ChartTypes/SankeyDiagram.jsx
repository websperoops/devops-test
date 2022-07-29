import Highcharts from 'highcharts'
import Sankey from 'highcharts/modules/sankey'
import BaseChart from './BaseChart';
import lineChartTheme from '../ChartThemes/LineChartTheme'

Sankey(Highcharts)

class SankeyDiagram extends BaseChart {
    _createSeries(chartData) {
        let toGroup = chartData.map(cd => [
            (this.props.groupName ? (this.props.groupName + ': ') : '') + cd[this.props.groupFieldName],
            cd[this.props.xFieldName],
            Number.parseFloat(cd[this.props.yFieldName])
        ])
        let uniqNames = Array.from(new Set(toGroup.map(d => d[0])));
        let series = uniqNames.map(name => (
            {
                "name": name,
                "data": toGroup.filter(cd => cd[0] == name).map(cd => [cd[0], cd[1], cd[2]])
            }
        )
        )
        return [{
            keys: ['from', 'to', 'weight'],
            data: series[0].data
        }]
    }

    get_options() {
        return {
            ...lineChartTheme,
            credits: {
                enabled: false
            },
            chart: {
                type: 'sankey'
            },
            id: this.props.chartId,
            title: {
                text: null,
                align: 'center',
            },
            subtitle: {
                // If subtitle is empty, Highcharts will put the chart in tha place where would be subtitle otherwive. We want to keep the size and place of chart stable in this case.
                // Therfore there is a transparent span for that. (Empty sign or spam would Highchart ignore)
                text: ((this.props.title) || (this.props.title !== undefined)) ? this.props.title : '<span style="opacity:0;">.</span>'
            },
        }
    }
}

export default SankeyDiagram;