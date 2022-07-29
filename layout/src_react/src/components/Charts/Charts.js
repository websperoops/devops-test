import React, { useEffect, useState, useContext, useLayoutEffect, Suspense } from 'react';
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official';
import { ReducerContext } from '../../index';
import { resizeHighchart } from '../../functions/dashboard/dashFunctions'


function Chart({ data, type, id, dimensions }) {
    const [options, setOptions] = useState()
    const [currentChart, setCurrentChart] = useState()
    const { state } = useContext(ReducerContext)

    useLayoutEffect(() => {
        if (data) {
            loaded_chart_containers.push(`${id}_container`);
            window.$(`#${id}_menu h5`).text(data.title);
        }

        Highcharts.Options = state.chartDetails.filter(chart => chart.type === type.toLowerCase())[0].options(data, id);
        setOptions(Highcharts.Options)


    }, [data])

    useEffect(() => {
        window.$(document).ready(function () {

            const chartIndex = Highcharts.charts.findIndex(chart => chart.userOptions.id === id);
            const chart = Highcharts.charts[chartIndex]
            setCurrentChart(chart)

            if (type != 'table' && type != 'single_metric') {
                // Clear previous all data series
                while (chart.series.length > 0) {
                    chart.series[0].remove();
                }
            }
            state.chartDetails.filter(t => t.type == type.toLowerCase())[0].createSeries(chart, data, type.toLowerCase() === 'stacked_column' && 'Stacked_Column')
        });


    }, [data])

    useEffect(() => { //resize charts initially on page load

        if (dimensions) {
            $(document).ready(function () {
                resizeHighchart(id)
            })
        }
    }, [data])

    return (
        <div id={`${id}_block`} className="d-flex" style={{ minHeight: 500 }} >
            <HighchartsReact
                highcharts={Highcharts}
                options={options}
            />
        </div>
    )
}


//Function for all charts -- see dashFunctions for draggable resize logic
// const resizeChart = (chart, dimensions, id) => {
//     chart.update({
//         chart: {
//             height: dimensions.height * 0.65,
//             width: dimensions.width * 0.90,
//         },
//         title: {
//             text: '', //get rid of the title 
//             align: 'center'

//         },
//     });

//     // chart.setSize(600);
//     chart.reflow();


// }

export default Chart;