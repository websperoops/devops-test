import React, { useState } from 'react';
import './summaryMetrics.css'; 

function MetricHeader({ integration, count,
    //   viewModal 
}) {
    const [json, setJson] = useState();


    return (
        <div className="menu" id={count + "_menu"}>
            <h5 className="text-capitalize" id={count + "_widgetHeader"}><img className="integration-img" src={`../../../../static/images/${integration}-icon.png`}/>{integration}</h5>
            <div className="graph-menu-icons"> 
            </div>
        </div>
    )
}

export default MetricHeader

