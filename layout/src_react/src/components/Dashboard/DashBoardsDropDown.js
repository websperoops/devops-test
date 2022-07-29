import React from 'react'
import "./dashMainPage.css";

function DashboardsDropDown(props) {
    return (
        <ul className="dash-dropdown"
            style={{ height: props.showDropDown && '120px', border: props.showDropDown && '1px solid #ddd' }}>
            {dashboards.map((dash, i) => {
                return <li key={i} onClick={() => props.dashChange(dash.id)}><i className={window.location.href.indexOf(dash.id) > -1 ? 'fa fa-check' : null}></i><p>{dash.title}</p></li>
            })}
        </ul>
    )
}

export default DashboardsDropDown;