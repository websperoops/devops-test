import React from 'react'
import "./dashMainPage.css";

function DashWidgetRating(props) {
    return (
        <div id={props.id + "_contentRating"} className="shader rating-box">
            <a title={props.id + "_closeRating"} id={props.id + "_closeRating"} className="rating-close icon" onClick={(e) => { linkElementClose(props.id) }}>
                <i className="ti-close"></i>
            </a>
            <div className="shader-content">
                <h3>Help us improve Blocklight!</h3>
                <h4>Is this Metric Helpful?</h4>
                <div className="row thumb-row justify-content-center">
                    <div className="col-xs-4">
                        <a title={props.id + "_thumbsUp"} id={props.id + "_thumbsUp"} className="thumb-up none" onClick={(e) => { submitGoodMetricFeedback(props.id) }}>
                            <i className="ti-thumb-up"></i>
                        </a>
                    </div>
                    <div className="col-xs-4">
                        <a title={props.id + "_thumbsDown"} id={props.id + "_thumbsDown"} className="thumb-down none" onClick={(e) => { submitBadMetricFeedback(props.id) }}>
                            <i className="ti-thumb-down"></i>
                        </a>
                    </div>
                </div>
                <h4 className="feedback-message" style={{ display: "none" }}>Thanks for your Feedback!</h4>
            </div>
        </div>

    )

}

export default DashWidgetRating;