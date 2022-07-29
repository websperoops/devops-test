import React, { useState, useEffect, Fragment } from 'react'
import MetricHeader from './MetricHeader';
import Summary_Metric from './Summary_Metric'
import { getDataSourceList, getChartDataTimeRange } from '../../api/BLApi';
import './summaryMetrics.css'; 

const HomePageSummary = ({metricProps, timeOption, time, id }) => {
    const [value, setValue] = useState('')
    const [previousValue, setPreviousValue] = useState('')
    const [loading, setLoading] = useState(true)

    useEffect(()=>{
        getDataSourceList().then(res => {
            const datasource = res.find(r => r.id === metricProps.data_source)
            let { filter, group_by, aggregate } = metricProps
            const {since, until, compare_since, compare_until} = timeOption.find(option => option.name === time)
            let dynamic, sum

            if (time.includes('Year')) dynamic = 'year'
            else if(time.includes('Month')) dynamic = 'month'
            else dynamic = 'day'

            // get current value
            getChartDataTimeRange(datasource.url, group_by, aggregate, since, until, dynamic, filter).then(res => {
                sum = 0
                if(res[0]) {
                    res.forEach(r => sum = sum + Number(r[aggregate]))
                    setValue(sum)      
                }
                else setValue(0)
            })

            // get compare value
            getChartDataTimeRange(datasource.url, group_by, aggregate, compare_since, compare_until, dynamic, filter).then(res => {
                sum = 0
                if(res[0]) {
                    res.forEach(r => sum+=Number(r[aggregate]))
                    setPreviousValue(sum)
                }
                else setPreviousValue(0)
            })

            setLoading(false)
        })
    }, [time])

    return (
            <div className="chart-container homepage-chart-container ml-3" id={id + "_container"}>
                <div className="graph theme-widgets">
                    {
                        !loading && (
                            <Fragment>
                                <MetricHeader integration={metricProps.integration_name} />
                                <Summary_Metric value={value.toLocaleString()} name={metricProps.name} increase={value > previousValue ? true : false} isEqualToPrev={value === previousValue}/>
                            </Fragment>
                        )
                    }
                </div>
            </div>
    )
}

export default HomePageSummary
