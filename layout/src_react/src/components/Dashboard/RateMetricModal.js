import React from 'react'
import ReactModal from 'react-modal'

const RateMetricModal = (props) => {


    const submitMetricFeedback = async (feedback) => {
        // Make call to save feedback to DB
        var path = chart_feedback_url +
            "?topic=" + props.id +
            "&description=" + feedback;
        const res = await fetch(path);

        props.close(); //close after rating
    }

    return (
        <ReactModal ariaHideApp={false} isOpen={props.show} className="modal-outer" onRequestClose={props.close}>
            <div className="modal-inner">

                <h3 className="text-dark mt-3">Help us improve Blocklight!</h3>

                <p className="text-dark mt-3">Is this Metric Helpful?</p>

                <div className="d-flex flex-row justify-content-center mt-4">
                    <i onClick={() => submitMetricFeedback('good')} style={{ cursor: 'pointer' }} className="fa fa-thumbs-o-up fa-4x m-3 text-success"></i>
                    <i onClick={() => submitMetricFeedback('bad')} style={{ cursor: 'pointer' }} className="fa fa-thumbs-o-down fa-4x m-3 text-danger"></i>

                </div>
            </div>
        </ReactModal>

    )
}

export default RateMetricModal