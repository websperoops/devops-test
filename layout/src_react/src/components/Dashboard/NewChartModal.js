import React, { useEffect, useState } from 'react'
import ReactModal from 'react-modal';
import { requestNewChartOptions, csrf_token } from '../../functions/dashboard/dashFunctions';


function NewChartModal(props) {

    const [integration, setIntegration] = useState(null);
    const [integrations, setIntegrations] = useState(null);
    const [json, setJson] = useState(null);
    const [metrics, setMetrics] = useState(null)
    const [nums, setNums] = useState(null);
    const [accounts, setAccounts] = useState(null);
    const [charts, setCharts] = useState(null);
    const [values, setValues] = useState(null);
    const [times, setTimes] = useState(null);


    //selected values
    const [metric, setMetric] = useState(null);
    const [num, setNum] = useState(null);
    const [time, setTime] = useState(null);
    const [chart, setChart] = useState(null);
    const [value, setValue] = useState(null);
    const [account, setAccount] = useState(null)


    useEffect(() => {
        if (props.show) {
            requestNewChartOptions(props.dashId).then(res => {
                setJson(res);
                setIntegrations(res.integrations);
            })

        }
    }, [props.show])

    const handleSetIntegration = (val) => {
        setIntegration(val);
        setMetrics(json[val]);
    }

    const handleSetMetric = val => {
        setMetric(val);
        setNums(json[val].supported_nums)
        setAccounts(json[val].supported_accounts);
        setCharts(json[val].supported_chart_types);
        setValues(json[val].supported_values);
        setTimes(json[val].supported_time_periods)
    }

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
        props.close()
    }

    const addChart = async () => {
        const res = await fetch('/dashboards/newchart/', {
            method: 'POST',
            body: JSON.stringify({
                integration,
                metric,
                value,
                'num': 'N/A',
                'chart_type': chart,
                time,
                'account': 'N/A',
                'dash_id': props.dashId
            }),
            headers: {
                "X-CSRFToken": csrf_token,
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest'
            },
        });
        const json = await res.json();
        json.status_code == 200 && window.location.reload();

    }


    return (
        <ReactModal isOpen={props.show} className="modal-outer" ariaHideApp={false} shouldCloseOnEsc={true} onRequestClose={cancelChart}>
            <div className="modal-inner">
                <h2>Add a New Metric</h2>

                <div className="d-flex justify-content-center flex-column w-50 mx-auto mt-4 bg-light">
                    <label htmlFor="integrations">Integrations:</label>
                    <select id="integrations" onChange={(e) => handleSetIntegration(e.target.value)}>
                        <option>Integrations</option>
                        {integrations && integrations.map(integration => <option key={integration} value={integration}>{integration}</option>)}
                    </select>
                </div>

                {metrics && <div className="d-flex justify-content-center flex-column w-50 mx-auto mt-4 bg-light">
                    <label htmlFor="Metrics">Metrics:</label>
                    <select id="Metrics" onChange={(e) => handleSetMetric(e.target.value)}>
                        <option>Metrics</option>
                        {metrics.map(metric => <option key={metric} value={metric}>{metric}</option>)}
                    </select>
                </div>}
                <div className="d-flex flex-row justify-content-between">
                    {(accounts !== null && accounts[0] !== "N/A") && <div className="d-flex justify-content-center flex-column mx-auto mt-4 bg-light">
                        <label htmlFor="accounts">Accounts:</label>
                        <select id="accounts" onChange={(e) => setAccount(e.target.value)}>
                            <option>Accounts</option>
                            {accounts.map(account => <option key={account} value={account}>{account}</option>)}
                        </select>
                    </div>}

                    {(nums !== null && nums[0] !== "N/A") && <div className="d-flex justify-content-center flex-column mx-auto mt-4 ">
                        <label htmlFor="nums">Numbers:</label>
                        <select id="nums" onChange={(e) => setNumber(e.target.value)}>
                            <option>Accounts</option>
                            {nums.map(account => <option key={nums} value={nums}>{nums}</option>)}
                        </select>
                    </div>}

                    {(charts !== null) && <div className="d-flex justify-content-center flex-column mx-auto mt-4">
                        <label htmlFor="integrations">Charts:</label>
                        <select onChange={(e) => setChart(e.target.value)} className="">
                            <option>Charts</option>
                            {charts.map(chart => <option key={chart} value={chart}>{chart.replace(/_/g, ' ')}</option>)}
                        </select>
                    </div>}


                    {(times !== null) && <div className="d-flex justify-content-center flex-column mx-auto mt-4">
                        <label htmlFor="integrations">Times:</label>
                        <select onChange={(e) => setTime(e.target.value)} className="">
                            <option>Times</option>
                            {times.map(time => <option key={time} value={time}>{time.replace(/_/g, ' ')}</option>)}
                        </select>
                    </div>}

                    {(values !== null) && <div className="d-flex justify-content-center flex-column mx-auto mt-4">
                        <label htmlFor="integrations">Values:</label>
                        <select onChange={(e) => setValue(e.target.value)} className="">
                            <option>Values:</option>
                            {values.map(val => <option key={val} value={val}>{val.replace(/_/g, ' ')}</option>)}
                        </select>
                    </div>}

                </div>

                {(value && time && chart) && <div className="d-flex flex-row justify-content-center mx-auto mt-4">
                    <button onClick={addChart} className="btn_orange">Add</button>
                    <button onClick={cancelChart} className="btn_clear">Cancel</button>
                </div>}
            </div>
        </ReactModal>
    )
}

export default NewChartModal;
