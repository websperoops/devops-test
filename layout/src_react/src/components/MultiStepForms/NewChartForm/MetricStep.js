import React, { useState, useEffect } from 'react'

const MetricStep = ({ metrics, handleSetMetric, handleNextbtn, json, chartimgs, integration }) => {
    const [chosenMetric, setChosenMetric] = useState()

    const handleMetric = metric => {
        setChosenMetric(metric)
        handleSetMetric(metric)
        handleNextbtn(true)
    }
    useEffect(() => {
        handleNextbtn(false)
    }, [])


    return (
        <>
            <h4 style={{ opacity: '0.8' }}>What information do you want to see?</h4>
            <div className="d-flex flex-row mt-4 flex-wrap justify-content-center metric_item_container">
                {metrics && metrics.map(metric => {

                    const chartType = json[metric].supported_chart_types[Math.ceil(json[metric].supported_chart_types.length - 1)]
                    // const imgIndex = 
                    const imgIndex = chartimgs.findIndex(c => c.chart == chartType)
                    let imgpath = null
                    if (imgIndex > -1) {
                        imgpath = chartimgs[imgIndex].img
                    }
                    var useBiggerHeight = false
                    if (integration == 'Google' || integration == 'Shopify and Mailchimp' || integration == 'Shopify and Mailchimp and Facebook' || 'Shopify And Mailchimp And Instagram') {
                        useBiggerHeight = true
                    }


                    return (<div onClick={() => handleMetric(metric)} key={metric} className={"d-fex flex-column justify-content-center align-items-center " + (chosenMetric == metric ? 'border-yellow ' : '') + (useBiggerHeight ? 'metric_item_google' : 'metric_item')}>
                        <img width={35} height={35} src={imgpath} />
                        <p className="text-capitalize mt-2">{metric}</p>
                    </div>)
                })}
            </div>
        </>
    )

}

export default MetricStep;