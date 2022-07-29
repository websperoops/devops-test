import React from 'react'
import DashActionMenu from './DashActionMenu';

function DashWidgetMenu(props) {
    return (
        <div className="menu" id={props.id + "_menu"}>

            <h5>{props.title}</h5>
            <div className="graph-menu-icons">
                <DashActionMenu chart={props.chart} id={props.id} toggleModal={props.toggleModal} />
            </div>
        </div>
    )
}


export default DashWidgetMenu;