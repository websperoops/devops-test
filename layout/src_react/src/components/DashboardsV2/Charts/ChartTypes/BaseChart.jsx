import React, { Component } from 'react'
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official';

class BaseChart extends Component {

    changeGroupNamesMap = {
        "True": "Yes",
        "False": "No"
    }

    constructor(props) {
        super(props);
        this.state = {
            highchartOptions: {
                ...this.get_options(),
                series: this._createSeries(props.chartData)
            },
        }

    }

    get_options() {
        console.error('Overwrite get_options method!')
    }

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
                    const date = new Date(cd[1].replace(' ', 'T')) // replacing the space with the 'T' makes the date work on Iphone
                    const isDate = date instanceof Date && !isNaN(date.valueOf());
                    const xValue = isDate ? date.getTime() : cd[1];
                    return [xValue, cd[2]]
                })
            }
        ))
        return series
    }
    componentDidUpdate(prevProps) {
        if (!_.isEqual(prevProps.chartData, this.props.chartData)) { // only update the series when chartData from previous props and current props arent equal.
            this.setState({
                highchartOptions: {
                    ...this.state.highchartOptions,
                    subtitle: {
                        text: this.props.title
                    },
                    series: this._createSeries(this.props.chartData)
                },

            })
        } // figure out how to update HighchartsReact through this function
        // this runs when a chart is updated
        this.chart.reflow();

    }
    render() {
        return (
            <div className="d-flex justify-content-center mt-4 h-100">
                <HighchartsReact
                    highcharts={Highcharts}
                    containerProps={{ className: 'chartContainer' }}
                    options={this.state.highchartOptions}
                    callback={c => this.chart = c}
                />
            </div>
        )
    }
}

export default BaseChart;