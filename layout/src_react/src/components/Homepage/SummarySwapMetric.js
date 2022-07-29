import React from 'react'

function SummarySwapMetric(props) {
    return (
        <a title="Swap metric for another" className="edit" style={{ cursor: 'pointer' }} onClick={(e) => { showNewChartModal(props.count) }}>
            <i className="ti-exchange-vertical" />
        </a>
    )
}

export default SummarySwapMetric;