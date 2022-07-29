import React from 'react'
import "./dashMainPage.css";


function DashWidgetDescription(props) {
    return (
        <div id={props.id + "_contentInfo"} className="shader">
            <a title={props.id + "_closeInfo"} id={props.id + "_closeInfo"} className="icon info-close" onClick={(e) => { linkElementClose(props.id) }}>
                <i className="ti-close"></i>
            </a>
            <div className="shader-content">
                <h3>Metric Description</h3>
                <p>Coming soon.</p>
            </div>
        </div>
    )
}


export default DashWidgetDescription