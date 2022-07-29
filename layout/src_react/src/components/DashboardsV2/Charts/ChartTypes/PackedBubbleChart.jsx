import Highcharts from 'highcharts'
import HighchartsMore from 'highcharts/highcharts-more';
import BaseChart from './BaseChart';
import lineChartTheme from '../ChartThemes/LineChartTheme';

HighchartsMore(Highcharts);

class PackedBubbleChart extends BaseChart {
    // This component needs a _createSeries() for custom logic to format the data. Otherwise, we crash.
    _createSeries(chartData) {
        let toGroup = chartData.map(cd => [
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
        let series = uniqNames.map(name => ({
                "name": name,
                "data": toGroup.filter(cd => cd[0] == name).map(cd => {
                    console.log('cd', cd)
                    return cd[2]
                })
            }
        ))
        return series
    }
    
    get_options() {
        return {
            ...lineChartTheme,
            credits: {
                enabled: false
            },
            chart: {
                type: 'packedbubble',
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
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                    '<td style="padding:0"><b>{point.y}</b></td></tr>',
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
                packedbubble: {
                    minSize: '30%',
                    maxSize: '120%',
                    zMin: 0,
                    zMax: 1000,
                    layoutAlgorithm: {
                        splitSeries: false,
                        gravitationalConstant: 0.02
                    },
                    dataLabels: {
                        enabled: true,
                        format: '{point.name}',
                        filter: {
                            property: 'y',
                            operator: '>',
                            value: 250
                        },
                        style: {
                            color: 'black',
                            textOutline: 'none',
                            fontWeight: 'normal'
                        }
                    }
                }
            },
            responsive: {
                rules: [{
                    condition: {
                    },
                    chartOptions: {
                        legend: {
                            layout: 'horizontal',
                            align: 'center',
                            verticalAlign: 'bottom'
                        }
                    }
                }]
            }
        }
    }
}

export default PackedBubbleChart;