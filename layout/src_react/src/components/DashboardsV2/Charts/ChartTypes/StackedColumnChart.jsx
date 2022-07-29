import BaseChart from './BaseChart';
import StackedColumnChartTheme from '../ChartThemes/StackedColumnChartTheme';

class StackedColumnChart extends BaseChart {

    get_options() {
        return {
            ...StackedColumnChartTheme,
            credits: {
                enabled: false
            },
            id: this.props.chartId,
            chart: {
                type: 'column',
                spacingBottom: 25,
            },
            colors: ['#e98535', '#dd403a', '#456990', '#dfd6a7', '#36413e', '#698996', '#c17c74', '#247BA0', '#bcac9b', '#ffe0b5'],
            title: {
                text: null
            },
            subtitle: {
                // If subtitle is empty, Highcharts will put the chart in tha place where would be subtitle otherwive. We want to keep the size and place of chart stable in case.
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
                min: 0,
                title: {
                    text: this.props.yAxis_title,
                    style: {
                        color: '#ffffff'
                    }
                },
                stackLabels: {
                    enabled: true,
                    style: {
                        fontWeight: 'bold',
                        color: 'white',
                    },
                    y: -25
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                x: -30,
                verticalAlign: 'top',
                y: 25,
                floating: true,
                backgroundColor: 'rgba(255,255,255,0.8)',
                borderColor: '#CCC',
                borderWidth: 1,
                shadow: false
            },
            tooltip: {
                headerFormat: '<span style="font-size:12px">{point.key}</span><table><br>',
                pointFormat: this.props.chartType == 'Stacked_Column' ? '<tr> <td style="color:{series.color};padding:0">{series.name}: </td>' +
                    '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>' : '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.percentage:.0f}%)<br/>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true,
                xDateFormat: '%b %e, %Y'
            },
            plotOptions: {
                column: {
                    stacking: this.props.chartType == 'Stacked_Column' ? 'normal' : 'percentage',
                    dataLabels: {
                        enabled: false, // Turn back on to display labels all the time
                        color: 'white'
                    }
                }
            }
        }
    }

    componentDidMount() {
        if (this.props.chartName === 'Website Referrals by Source') {
            let { chartData } = this.props
            let newChartData = []
            let totals = {}

            chartData.forEach(cd => totals[cd.datehour__gt] = totals[cd.datehour__gt] ? parseInt(totals[cd.datehour__gt]) + parseInt(cd.users__sum) : parseInt(cd.users__sum)) // set totals per date
            chartData.forEach((cd, i) => {
                if (cd.source.toLowerCase().includes('instagram')) {
                    cd.source = 'Instagram';
                }
                else if (cd.source.toLowerCase().includes('facebook')) {
                    cd.source = 'Facebook';
                }
                else if (cd.source.toLowerCase().includes('google')) {
                    cd.source = 'Google'
                }
                if (cd.users__sum < totals[cd.datehour__gt] * .10) {
                    const index = newChartData.findIndex(c => c.source == 'Other' && c.datehour__gt == cd.datehour__gt);
                    if (index > -1) {
                        const sum = parseInt(newChartData[index].users__sum) + parseInt(cd.users__sum)
                        newChartData[index].users__sum = sum
                    }
                    else {
                        newChartData.push({ ...cd, source: 'Other' })
                    }
                }
                else {
                    newChartData.push({ ...cd })
                }

            })
            this.setState({
                highchartOptions: {
                    series: this._createSeries(newChartData)
                },
            })

        }
    }
}

export default StackedColumnChart;
