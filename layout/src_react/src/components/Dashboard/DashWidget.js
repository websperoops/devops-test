import React, { useState } from 'react'
import DashWidgetDescription from './DashWidgetDescription';
import DashWidgetRating from './DashWidgetRating';
import DashWidgetError from './DashWidgetError';
import DashWidgetShield from './DashWidgetShield';
import DashWidgetMenu from './DashWidgetMenu';
import DashWidgetContent from './DashWidgetContent';


function DashWidget(props) {

    return (
        <div className="chart-container draggable grid-stack-item ui-draggable ui-resizable ui-resizable-autohide"
            id={props.id + "_container"} style={{}}>
            <DashWidgetDescription id={props.id} />
            <DashWidgetRating id={props.id} />
            <DashWidgetError id={props.id} />
            <DashWidgetShield />
            <div className="graph theme-widgets">
                <DashWidgetMenu
                    chart={props.chart}
                    id={props.id}
                    title={props.title}
                    toggleModal={props.toggleModal} />
                <DashWidgetContent id={props.id} src={"/static/charts/" + props.type + ".html"} type={props.type} chart={props.chart} />
            </div>

        </div>
    )
}

export default DashWidget;