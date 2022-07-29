import React, { useEffect } from 'react';

function Single_Metric({ data, id, context }) {
    useEffect(() => {
        if (data) {
            window.$(`#${id}_menu h5`).text(data.title)
        }
    }, [data])


    return (
        <div className="text-dark single_metric_container" id={id + '_block'}>
            <p id='subtitle' style={{ fontSize: '12px', marginTop: '-20px' }} className="text-center font-weight-bold">{data.subtitle}</p>
            <div className="d-flex flex-row justify-content-center align-items-center">
                {data.data_label == '$' ? <><p style={{ fontSize: '2rem' }}>{data.data_label}</p> <p className="text-right" style={{ fontSize: '2rem', fontWeight: 'bold' }}>{data.series[0].data}</p></>
                    : <><p className="text-right" style={{ fontSize: '2rem', fontWeight: 'bold' }}>{data.series[0].data.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")}</p> <p className="ml-2" style={{ fontSize: '2rem' }}>{data.data_label}</p></>}
            </div>
        </div>

    )
}

export default Single_Metric;