
import React from 'react'
import BaseChart from './BaseChart';
import Highcharts from 'highcharts/highmaps'
import HighchartsReact from 'highcharts-react-official'
import mapData from '@highcharts/map-collection/countries/us/us-all.geo.json'

class USAMapChart extends BaseChart {

    _createSeries(chartData) {
        const stateMapping = {
            'Arizona': 'AZ',
            'Alabama': 'AL',
            'Alaska': 'AK',
            'Arkansas': 'AR',
            'California': 'CA',
            'Colorado': 'CO',
            'Connecticut': 'CT',
            'Delaware': 'DE',
            'Florida': 'FL',
            'Georgia': 'GA',
            'Hawaii': 'HI',
            'Idaho': 'ID',
            'Illinois': 'IL',
            'Indiana': 'IN',
            'Iowa': 'IA',
            'Kansas': 'KS',
            'Kentucky': 'KY',
            'Louisiana': 'LA',
            'Maine': 'ME',
            'Maryland': 'MD',
            'Massachusetts': 'MA',
            'Michigan': 'MI',
            'Minnesota': 'MN',
            'Mississippi': 'MS',
            'Missouri': 'MO',
            'Montana': 'MT',
            'Nebraska': 'NE',
            'Nevada': 'NV',
            'New Hampshire': 'NH',
            'New Jersey': 'NJ',
            'New Mexico': 'NM',
            'New York': 'NY',
            'North Carolina': 'NC',
            'North Dakota': 'ND',
            'Ohio': 'OH',
            'Oklahoma': 'OK',
            'Oregon': 'OR',
            'Pennsylvania': 'PA',
            'Rhode Island': 'RI',
            'South Carolina': 'SC',
            'South Dakota': 'SD',
            'Tennessee': 'TN',
            'Texas': 'TX',
            'Utah': 'UT',
            'Vermont': 'VT',
            'Virginia': 'VA',
            'Washington': 'WA',
            'West Virginia': 'WV',
            'Wisconsin': 'WI',
            'Wyoming': 'WY'
        }

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
        let series = uniqNames.map(name => (
            {
                "name": name,
                "data": toGroup.filter(cd => cd[0] == name).map(cd => {
                    return { code: cd[1].length > 2 ? stateMapping[cd[1]] : cd[1], value: cd[2] }
                })
            }
        ))

        return [{
            joinBy: ['postal-code', 'code'],
            mapData: mapData,
            data: series[0].data,
        }]
    }

    get_options() {
        return {
            credits: {
                enabled: false,
            },
            chart: {
                map: 'countries/us/us-all',
                borderWidth: 0
            },
            title: {
                text: null
            },
            subtitle: {
                // If subtitle is empty, Highcharts will put the chart in tha place where would be subtitle otherwive. We want to keep the size and place of chart stable in case.
                //    Therfore there is a transparent span for that. (Empty sign or spam would Highchart ignore)
                text: ((this.props.title) || (this.props.title !== undefined)) ? this.props.title : '<span style="opacity:0;">.</span>'
            },
            tooltip: {
                headerFormat: '<span style="font-size:12px;color: {point.color}">{point.key}</span><table>',
                pointFormat: '<div class="d-flex justify-content-center">{point.value}</div>',
                useHTML: true,
            },
            mapNavigation: {
                enabled: true
            },
            colorAxis: {
                min: 1,
                type: 'logarithmic',
                maxColor: '#eb8527',
                minColor: '#FFCA3D',
            },
        }
    }

    render() {
        return (
            <div className="d-flex justify-content-center mt-4 h-100" >
                <HighchartsReact
                    highcharts={Highcharts}
                    containerProps={{ className: 'chartContainer' }}
                    options={this.state.highchartOptions}
                    callback={c => this.chart = c}
                    constructorType="mapChart"
                />
            </div>
        )
    }


}

export default USAMapChart;