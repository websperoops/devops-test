import React, { useState, useEffect } from 'react'
import AccountStep from './AccountStep'
import MetricStep from './MetricStep'
import DataStep from './DataStep'
import TypeStep from './TypeStep'
import TimeStep from './TimeStep'
import ReactModal from 'react-modal'
import { requestNewChartOptions, csrf_token } from '../../../functions/dashboard/dashFunctions';



const NewChartForm = (props) => {
    const [currentStep, setCurentStep] = useState(0)
    const [integration, setIntegration] = useState(null);
    const [integrations, setIntegrations] = useState(null);
    const [json, setJson] = useState(null);
    const [metrics, setMetrics] = useState(null)
    const [nums, setNums] = useState(null);
    const [accounts, setAccounts] = useState(null);
    const [charts, setCharts] = useState(null);
    const [values, setValues] = useState(null);
    const [times, setTimes] = useState(null);
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


    const [nextBtn, setNextBtn] = useState(true)

    //selected values
    const [metric, setMetric] = useState(null);
    const [num, setNum] = useState(null);
    const [time, setTime] = useState(null);
    const [chart, setChart] = useState(null);
    const [value, setValue] = useState(null);
    const [account, setAccount] = useState(null)

    const handleNextbtn = (bool) => (setNextBtn(bool))


    useEffect(() => {
        if (props.dashId) {
            requestNewChartOptions(props.dashId).then(res => {
                setJson(res);
                setIntegrations(res.integrations);
            })

        }
    }, [props.dashId])

    const cancelChart = () => { //reset options on cancelling 
        setNums(null);
        setAccounts(null);
        setCharts(null);
        setValues(null);
        setTimes(null);
        setIntegration(null);
        setMetrics(null);
        setTime(null);
        setValue(null);
        setChart(null);
        setCurentStep(0)
        props.close()
    }

    const handleValueChange = (val) => {
        setValue(val)
    }

    const handleTimeChange = (val) => {
        setTime(val)
    }
    const addChart = async () => {
        const res = await fetch('/dashboards/newchart/', {
            method: 'POST',
            body: JSON.stringify(
                {
                    integration,
                    metric,
                    value,
                    'num': 'N/A',
                    'chart_type': chart,
                    time,
                    'account': 'N/A',
                    'dash_id': props.dashId
                }
            ),
            headers: {
                "X-CSRFToken": csrf_token,
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest'
            },
        });
        const json = await res.json();
        json.status_code == 200 && window.location.reload();

    }
    const handleSetIntegration = (val) => {

        setIntegration(val);
        setMetrics(json[val]);

        console.log(json[val])
    }

    const handleSetMetric = val => {
        setMetric(val);
        setNums(json[val].supported_nums)
        setAccounts(json[val].supported_accounts);
        setCharts(json[val].supported_chart_types);
        setValues(json[val].supported_values);
        setTimes(json[val].supported_time_periods)
    }


    const handleSetChart = chart => {
        setChart(chart)
    }


    const steps = [<AccountStep />, <MetricStep />, <DataStep />, <TypeStep />, <TimeStep />]

    const showStep = () => {
        console.log(currentStep)
        switch (currentStep) {
            case 0:
                return <AccountStep integrations={integrations} handleSetIntegration={handleSetIntegration} handleNextbtn={handleNextbtn} />
                break;
            case 1:
                return <MetricStep metrics={metrics} handleSetMetric={handleSetMetric} handleNextbtn={handleNextbtn} chartimgs={chartimgs} json={json} integration={integration} />
                break;
            case 2:
                return <DataStep values={values} handleValueChange={handleValueChange} handleNextbtn={handleNextbtn} />
                break;
            case 3:
                return <TypeStep charts={charts} handleSetChart={handleSetChart} handleNextbtn={handleNextbtn} chartimgs={chartimgs} />
                break
            case 4:
                return <TimeStep times={times} handleTimeChange={handleTimeChange} />
                break;
            default:
                return null;
        }
    }

    return (
        <ReactModal className="modal-outer multistep-form-modal" isOpen={props.show} ariaHideApp={false} shouldCloseOnEsc={true} onRequestClose={cancelChart}>
            <div className="modal-inner">
                <h2 className="text-center">Add A New Metric</h2>
                <div>
                    <div className="navigation-step d-flex flex-row justify-content-center mt-3 mb-3">
                        <div className="navigation-step-item">Account</div>
                        <div className={"navigation-step-item " + (currentStep >= 1 ? 'navigation-step-item-complete' : null)}>Metric</div>
                        <div className={"navigation-step-item " + (currentStep >= 2 ? 'navigation-step-item-complete' : null)}>Data</div>
                        <div className={"navigation-step-item " + (currentStep >= 3 ? 'navigation-step-item-complete' : null)}>Type</div>
                        <div className={"navigation-step-item " + (currentStep >= 4 ? 'navigation-step-item-complete' : null)}>Time</div>
                    </div>
                    {showStep()}
                </div>
                <div className="d-flex flex-row justify-content-end w-75 mx-auto">
                    <button className="btn_clear" disabled={currentStep == 0} onClick={() => setCurentStep(currentStep - 1)}>Back</button>
                    {currentStep < 4 && <button disabled={!(nextBtn)} className={"btn_orange " + (!nextBtn ? 'btn_gray' : null)} onClick={() => setCurentStep(currentStep + 1)}>Next</button>}
                    {(currentStep == 4) && <button disabled={!(metric && chart && time)} className="btn_orange" onClick={addChart}>Finish</button>}

                </div>
            </div>
        </ReactModal >
    )

}

export default NewChartForm