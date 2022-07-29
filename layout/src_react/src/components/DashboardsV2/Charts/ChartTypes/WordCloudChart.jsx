import BaseChart from './BaseChart'
import Highcharts from 'highcharts'
import WC from 'highcharts/modules/wordcloud';
import lineChartTheme from '../ChartThemes/LineChartTheme';

WC(Highcharts)

class WordCloudChart extends BaseChart {
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
                "data": toGroup.filter(cd => cd[0] == name).map(cd => {
                    return {
                        name: cd[1],
                        weight: cd[2]
                    }
                })
            }
        )
        )
        return series
    }

    get_options() {
        return {
            ...lineChartTheme,
            credits: {
                enabled: false
            },
            id: this.props.chartId,
            chart: {
                type: 'wordcloud',
            },
            plotOptions: {
                wordcloud: {
                    minFontSize: 10,
                    maxFontSize: 40
                },
            },
            title: {
                text: null
            },
            subtitle: {
                // If subtitle is empty, Highcharts will put the chart in tha place where would be subtitle otherwive. We want to keep the size and place of chart stable in case.
                // Therfore there is a transparent span for that. (Empty sign or spam would Highchart ignore)
                text: ((this.props.title) || (this.props.title !== undefined)) ? this.props.title : '<span style="opacity:0;">.</span>'
            }
        }
    }
}

export default WordCloudChart