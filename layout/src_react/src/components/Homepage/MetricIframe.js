import React from 'react';


function MetricIframe(props) {
    return (
        <div className="grid-stack-item-content" id={props.count + "_gridContent"}>
            <li id={props.count + "_widget"} className="widget">
                <div id={props.count + "_widget-content"} className="widget-content">
                    <iframe id={props.count + "_iframe"} className="widget-iframe" src="/static/charts/Single_Metric.html" title={props.title} />
                </div>
            </li>
        </div>
    )
}
export default MetricIframe;