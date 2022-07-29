import BaseChart from './BaseChart';
import Tree_map from 'highcharts/modules/treemap'
import Highcharts from 'highcharts'

Tree_map(Highcharts)

class Treemap extends BaseChart {
    _createSeries(chartData) {
        const chartDataFiltered = chartData.filter(item => item.country_code === 'US')
        let toGroup = chartDataFiltered.map(cd => [
            (this.props.groupName ? (this.props.groupName + ' ') : '')
            + (
                this.props.groupFieldName
                    ? (
                        Object.keys(this.changeGroupNamesMap).includes(cd[this.props.groupFieldName])
                            ? this.changeGroupNamesMap[cd[this.props.groupFieldName]]
                            : cd[this.props.groupFieldName]
                    )
                    : ''),
            cd[this.props.xFieldName],
            Number.parseFloat(cd[this.props.yFieldName])
        ])
        const uniqNames = Array.from(new Set(toGroup.map(d => d[0])));
        let series = uniqNames.map(name => (
            {
                "name": name,
                "data": toGroup.filter(cd => cd[0] == name).map(cd => {
                    console.log(cd)
                    return { name: cd[1], value: cd[2], colorValue: cd[2] }

                })
            }
        ))
        return [
            {
                type: 'treemap',
                data: series[0].data,
                layoutAlgorithm: 'squarified',
            }
        ]
    }

    get_options() {
        return {
            credits: {
                enabled: false
            },
            colorAxis: {
                minColor: '#FFFFFF',
                maxColor: '#ef7c15'
            },
            chart: {
                spacingBottom: 25,
            },
            title: {
                text: null,
                align: 'center',
            },
            id: this.props.chartId,
            subtitle: {
                // If subtitle is empty, Highcharts will put the chart in tha place where would be subtitle otherwive. We want to keep the size and place of chart stable in case.
                // Therfore there is a transparent span for that. (Empty sign or spam would Highchart ignore)
                text: ((this.props.title) || (this.props.title !== undefined)) ? this.props.title : '<span style="opacity:0;">.</span>'
            },
        }
    }
}

export default Treemap;
