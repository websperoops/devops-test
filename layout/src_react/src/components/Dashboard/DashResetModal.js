import React from 'react'
import ReactModal from 'react-modal';
import { resizeHighchart } from '../../functions/dashboard/dashFunctions'
import $ from 'jquery'

function DashResetModal(props) {

    const close = () => props.close();
    const resetDashboardLayout = () => {
        const grid = $('.grid-stack').data('gridstack')
        grid.batchUpdate();

        const charts = $('.chart-container')
        let chart_ids = [];
        let xLoc = 0
        let yLoc = 0
        for (let i = 0; i < charts.length; i++) {
            grid.update(charts[i], xLoc, yLoc, 4, 4)
            if (xLoc < 8) {
                xLoc = xLoc + 4
            } else {
                xLoc = 0
                yLoc = yLoc + 4
            }
            chart_ids.push(charts[i].id.split('_container')[0])
        }
        grid.commit();

        setTimeout(() => {
            chart_ids.map(id => resizeHighchart(id))
        }, 500)

        close();
    }

    return (<ReactModal ariaHideApp={false}
        shouldCloseOnEsc={true}
        onRequestClose={close}
        isOpen={props.show}
        className="modal-outer" >
        <div className="modal-inner" >
            <h3 className="mb-3" > Reset Dashboard Layout? </h3>
            <div className="d-flex flex-row justify-content-center">
                <button onClick={resetDashboardLayout} className="btn_orange" > Reset! </button>
                <button onClick={close} className="btn_clear" > Cancel </button>
            </div>
        </div>
    </ReactModal >
    )
}

export default DashResetModal