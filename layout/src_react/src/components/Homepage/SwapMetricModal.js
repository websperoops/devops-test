import React, { useContext, useState } from 'react'
import ReactModal from 'react-modal';
import { changeSummaryTime } from '../../functions/homepage/homepageFunctions';
import './summaryMetrics.css'; 

function SwapMetricModal(props) {
    const [time, setTime] = useState(null);
    const changeMetric = () => {
        props.updateData(changeSummaryTime(props.chart, time, props.count)) //updates summary data
        props.closeModal()
    }

    return (
        <ReactModal ariaHideApp={false} onRequestClose={props.closeModal} className="modal-outer" isOpen={props.showModal} shouldCloseOnEsc={true} shouldCloseOnOverlayClick={true}>
            <div className="modal-inner">
                <h3 className="select-time">Select Time</h3>
                <div className="select-time-area">
                    <select style={{ width: '140px' }} className="mt-0" onChange={(e) => setTime(e.target.value)}>
                        {props.supportedTimes.map(time => <option key={time} value={time}>{time.replace(/_/g, ' ')}</option>)}
                    </select>

                    <button onClick={changeMetric} className="btn_orange">Go!</button>
                </div>
            </div>
        </ReactModal>
    )
}

export default SwapMetricModal