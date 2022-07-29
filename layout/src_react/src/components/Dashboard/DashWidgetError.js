import React from 'react'
import "./dashMainPage.css";


function DashWidgetError(props) {
    return (
        <div id={props.id + "_loadErrorDiv"} className="shader" style={{ visibility: "hidden" }}>


            <div className="shader-content">
                <h3>Oh no!</h3>
                <p>There is inadequate data for this chart. Please try changing the date range.</p>
                <p id={props.id + "_loadErrorMsg"}></p>
            </div>
        </div>

    )
}

export default DashWidgetError;