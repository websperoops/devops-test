import React from 'react'
import BaseChart from './BaseChart';
import Highcharts from 'highcharts/highmaps'
import HighchartsReact from 'highcharts-react-official'
import mapData from '@highcharts/map-collection/custom/world.geo.json'
import { countries } from 'country-data';


class WorldMap extends BaseChart {
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
        let series = uniqNames.map(name => (
            {
                "name": name,
                "data": toGroup.filter(cd => cd[0] == name).map(cd => {
                    return { code: countries[cd[1]].alpha3, value: cd[2] }
                })
            }
        ))

        return [{
            joinBy: ['iso-a3', 'code'],
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
                map: 'custom/world',
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

export default WorldMap;
