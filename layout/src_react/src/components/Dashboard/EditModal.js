import React, { useState, useEffect, useContext } from 'react'
import ReactModal from 'react-modal';
import { ReducerContext } from '../../index'
import "./dashMainPage.css";


function EditModal(props) {
    const { state, dispatch } = useContext(ReducerContext)

    const [chartimgs, setChartimgs] = useState([
        { chart: 'Pie', img: '/static/images/piechart.svg' },
        { chart: 'Table', img: '/static/images/table.svg' },
        { chart: 'Column', img: '/static/images/columngraph.svg' },
        { chart: 'Stacked_Column', img: '/static/images/stackedcolumn.svg' },
        { chart: 'Area', img: '/static/images/area.svg' },
        { chart: 'Dual_Axis', img: '/static/images/dualaxischart.svg' },
        { chart: 'Line', img: '/static/images/linegraph.svg' },
        { chart: 'Single_Metric', img: '/static/images/number.svg' },
        { chart: 'USA_Map', img: '/static/images/map.svg' }


    ])

    const [times, setTimes] = useState([]);
    const [data, setData] = useState([]);
    const [charts, setCharts] = useState([]);
    const [dashboards, setDashboards] = useState([]);

    const [selectedTime, setSelectedTime] = useState();
    const [selectedData, setSelectedData] = useState();
    const [selectedChart, setSelectedChart] = useState();


    const submitChanges = () => {
        // updateChartTimePeriod(props.chart, newData)
        const { chart } = props
        const chartType = selectedChart || chart.current_chart_type;
        if (chart.current_option == null) {
            var option = data.length && selectedData ? `{%27value%27:%27${selectedData}%27}` : '{}'
        } else {
            var option = data.length && selectedData ? `{%27value%27:%27${selectedData}%27}` : `{%27value%27:%27${chart.current_option.value}%27}`
        }
        const time = selectedTime || chart.current_time_period

        console.log(chart, data)

        var path = chart_data_url +
            "?chart_id=" + chart.id +
            "&integration=" + chart.integration +
            "&metric=" + chart.metric +
            "&option=" + option +
            "&chart_type=" + chartType +
            "&time_period=" + time +
            "&dashboard_id=" + chart.dashboard +
            "&what_changed=" + 'everything';


        dispatch({ type: 'chartUpdate', payload: { chart, path, chartType } })
        console.log(path)
        props.close()
    }



    useEffect(() => {

        setTimes(props.chart.supported_time_periods)
        props.chart.supported_options && (props.chart.supported_options.value && setData(props.chart.supported_options.value))
        props.chart.supported_chart_types && setCharts(props.chart.supported_chart_types)
    }, [props.chart])

    console.log(data)

    return (
        <ReactModal ariaHideApp={false} isOpen={props.show} className="modal-outer" onRequestClose={props.close}>
            <div className="modal-inner edit-metric-modal">
                <h3>Edit Metric</h3>

                <div className="d-flex flex-column justify-content-center edit-metric-container mt-3">
                    <div className="d-flex flex-column justify-content-center">
                        <div className="edit-metric-header-container">
                            <p className="text-left ml-2 mt-1">Data</p>
                        </div>
                        <div className="d-flex flex-column justify-content-center">
                            <p>What information do you wish to see?</p>
                            <select disabled={!data.length} className="mx-auto mb-3" onChange={e => setSelectedData(e.target.value)}>
                                <option>Data</option>
                                {data.map((d, i) => <option key={i} value={d}>{d.replace(/_/g, ' ')}</option>)}
                            </select>
                        </div>
                    </div>

                    <div className="d-flex flex-column justify-content-center">
                        <div className="edit-metric-header-container">
                            <p className="text-left ml-2 mt-1">Type</p>
                        </div>
                        <div className="d-flex flex-row mt-4 flex-wrap justify-content-center">
                            {charts && charts.map(chart => {
                                const index = chartimgs.findIndex(c => c.chart == chart);
                                let imgPath = null
                                if (index > -1) {
                                    imgPath = chartimgs[index].img
                                }
                                return (
                                    <div key={chart} onClick={() => setSelectedChart(chart)} className={"edit_type_item d-fex flex-column justify-content-center align-items-center mb-3 " + (selectedChart == chart ? 'border-yellow' : '')}>
                                        <img className='mx-auto' width={35} height={35} src={`${imgPath}`} />
                                        <p className="text-capialize mt-2">{chart.replace(/_/g, ' ')}</p>
                                    </div>
                                )
                            })}
                        </div>
                    </div>

                    <div className="d-flex flex-column justify-content-center">
                        <div className="edit-metric-header-container">
                            <p className="text-left ml-2 mt-1">Time</p>
                        </div>
                        <div className="d-flex flex-column justify-content-center">
                            <select disabled={times.length == 1 && times[0] == 'All_Time'} className="mx-auto mb-3" onChange={e => setSelectedTime(e.target.value)}>
                                {times.length == 1 && times[0] == 'All_Time' ? <option> All Time </option> : <option>Times</option>}
                                {times && times.map(time => <option key={time} value={time}>{time.replace(/_/g, ' ')}</option>)}
                            </select>
                        </div>
                    </div>
                </div>
                {/* <div className="d-flex flex-row flex-wrap justify-content-around">
                    {data !== null &&
                        <div className="d-flex flex-column mt-2" style={{ width: '150px' }}>
                            <label htmlFor="data-type">Data Type:</label>

                            <select id="data-type" onChange={e => setSelectedData(e.target.value)}>
                                <option>Data</option>

                                {data.map(d => <option key={d} value={d}>{d.replace(/_/g, ' ')}</option>)}
                            </select>
                        </div>
                    }
                    {times &&
                        <div className="d-flex flex-column mt-2" style={{ width: '150px' }}>
                            <label htmlFor="time">Time:</label>

                            <select id="time" onChange={e => setSelectedTime(e.target.value)}>
                                <option>Times</option>

                                {times.map(time => <option key={time} value={time}>{time.replace(/_/g, ' ')}</option>)}
                            </select>
                        </div>
                    }
                    {charts &&
                        <div className="d-flex flex-column mt-2" style={{ width: '150px' }}>
                            <label htmlFor="chart-type">Chart Type:</label>
                            <select id="chart-type" onChange={e => setSelectedChart(e.target.value)}>
                                <option>Charts</option>
                                {charts.map(chart => <option key={chart} value={chart}>{chart.replace(/_/g, ' ')}</option>)}

                            </select>
                        </div>
                    }
                </div>

                <button onClick={submitChanges} className="btn_orange">Submit</button> */}
                <div className="d-flex flex-row justify-content-end">
                    <button onClick={props.close} className="btn_clear">Back</button>
                    <button onClick={submitChanges} className="btn_orange">Save</button>
                </div>


            </div>

        </ReactModal>
    )

}

export default EditModal;