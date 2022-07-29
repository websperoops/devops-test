import BaseChart from './BaseChart';
import PieChartTheme from '../ChartThemes/PieChartTheme'


class PieChart extends BaseChart {
    _createSeries(chartData) {
        let toGroup = chartData.map(cd => [
            (this.props.groupName ? (this.props.groupName + ': ') : '') + cd[this.props.groupFieldName],
            cd[this.props.xFieldName],
            parseFloat(cd[this.props.yFieldName])
        ])
        let uniqNames = Array.from(new Set(toGroup.map(d => d[0])));
        let series = uniqNames.map(name => (
            {
                "name": name,
                "data": toGroup.filter(cd => cd[0] == name).map(cd => {
                    if (cd[1] !== null && cd[1].length > 0) {
                        var nameVal = cd[1]
                    }
                    else {
                        var nameVal = 'N/A'
                    }
                    return {
                        name: nameVal,
                        y: cd[2],
                    }
                })
            }
        )
        )
        return series
    }

    get_options() {
        return {
            ...PieChartTheme,
            credits: {
                enabled: false
            },
            id: this.props.chartId,
            responsive: {
                rules: [{
                    condition: {
                        maxHeight: 190
                    },
                    chartOptions: {
                        title: {
                            text: null
                        },
                        plotOptions: {
                            pie: {
                                dataLabels: {
                                    enabled: false,
                                },
                            }
                        }
                    }
                }]
            },
            chart: {
                type: 'pie',
                marginBottom: 20 //so labels dont get cut off when theres lots of them
            },
            title: {
                text: null
            },
            subtitle: {
                // If subtitle is empty, Highcharts will put the chart in tha place where would be subtitle otherwive. We want to keep the size and place of chart stable in case.
                // Therfore there is a transparent span for that. (Empty sign or spam would Highchart ignore)
                text: ((this.props.title) || (this.props.title !== undefined)) ? this.props.title : '<span style="opacity:0;">.</span>'
            },
            tooltip: {
                pointFormat: '{point.percentage:.1f} %'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        format: '<b>{point.name}</b>: {point.y}'
                    }
                }
            }
        }
    }
}

export default PieChart;
