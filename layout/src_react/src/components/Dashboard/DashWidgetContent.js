import React, { useContext, useState, useEffect } from 'react'
import Chart from '../Charts/Charts';
import Single_Metric from '../Charts/Single_Metric';
import { ReducerContext } from '../../index';
import { dataTableLoad } from '../../functions/dashboard/dashFunctions';
import Table from '../Charts/DataTable'
import "./dashMainPage.css";


function DashWidgetContent(props) {
    const [iframe, setIframe] = useState(null)
    const [data, setData] = useState();
    const el = React.useRef(el);
    const [width, setWidth] = useState(0);
    const [height, setHeight] = useState(0);
    const [type, setType] = useState(props.type)

    const { state, dispatch } = useContext(ReducerContext);

    // useEffect(() => {
    //     if (loaded_chart_containers.length >= all_chart_containers.length || !blocklight_data || all_chart_containers.length == 0) {
    //         window.$(".bubblingG").fadeOut();
    //         window.$(".spinner-wrapper").delay(500).fadeOut("slow");
    //     }

    // })


    useEffect(() => {
        if (iframe !== null && data) {
            iframe.onload = () => {
                dataTableLoad(props.id, data)
            }
        }

    }, [iframe, data])



    const updateData = async () => {
        setType(state.chartUpdate.chartType)

        if (state.chartUpdate.path.indexOf('google') > -1) {
            state.chartUpdate.path = state.chartUpdate.path.replace('Past_1_Day', 'Past_Day')
        }
        if (state.chartUpdate.path.indexOf('#') > -1) {
            state.chartUpdate.path = state.chartUpdate.path.replace(/#/g, '%23')
        }
        if (state.chartUpdate.path.indexOf('option={%27value%27:%27undefined%27}' > -1) && props.chart.current_option) {
            state.chartUpdate.path = state.chartUpdate.path.replace('undefined', props.chart.current_option.value);
        }
        const res = await fetch(state.chartUpdate.path.replace(/#/g, '%23'));
        const json = await res.json();
        setData(json) //find way to not add to loadedlist instead replace the old one

    }

    useEffect(() => {
        if (state.chartUpdate !== null && state.chartUpdate.chart.num_id == props.chart.num_id) {
            updateData()
        }
    }, [state.chartUpdate])

    useEffect(() => {
        props.chart.json.then(json => setData(json))
        setDimensions()
    }, [])

    // setTimeout(setDimensions, 100) //run one time on initial load


    const setDimensions = () => {
        setWidth(window.$(`#${props.id}_container`).width())
        setHeight(window.$(`#${props.id}_container`).height())
    }




    $('#resetDash').click(function () {
        setTimeout(setDimensions, 400) //get correct width and height
    })

    $('.grid-stack').on('gsresizestop', function () {
        setDimensions()
    });

    $(window).on('resize', function () {
        setDimensions()
    });


    function chartType() {
        if (props.src.indexOf("Single_Metric") > -1 && data) {
            return <Single_Metric data={data} id={props.id} dimensions={{ height, width }} />
        }
        else if (props.src.indexOf('Table') > -1 && data) {
            // return <iframe id={props.id + "_iframe"} className="widget-iframe" style={{ overflow: "hidden", border: "none" }} src={props.src} ref={(f) => setIframe(f)}> </iframe>
            return <Table id={props.id} data={data} style={{ overflow: "auto", border: "none" }}/>
        }

        else if (data) {
            return <Chart type={type} data={data} dimensions={{ height, width }} id={props.id} />
        }

    }



    return (
        <div className="grid-stack-item-content dash-widget-content" id={props.id + "_gridContent"} ref={el}>
            <li id={props.id + "_widget"} className="widget" ref={el}>
                <div id={props.id + "_widget-content"} className="widget-content widget-chart-type">
                    {chartType()}
                </div>
            </li>
        </div>

    )
}

export default DashWidgetContent;