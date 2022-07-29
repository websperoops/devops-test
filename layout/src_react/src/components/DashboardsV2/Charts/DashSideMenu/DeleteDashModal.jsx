import React, { Component } from 'react'
import ReactModal from 'react-modal';
import { deleteDashboard } from '../../../../api/BLApi'

class DeleteDashModal extends Component {

    constructor(props) {
        super(props);
        this.handleDelete = this.handleDelete.bind(this)
        this.handleClose = this.handleClose.bind(this)
    }

    handleClose() {
        this.props.closeFunc()
    }

    handleDelete() {
        deleteDashboard(this.props.dashboardId).then(data => {
            window.location.href = `${window.location.origin}/dashboards/v2/${this.props.dashboardsList[0].id}`
        }).catch((err) => { console.error(err) })

    }

    render() {
        return (
            <ReactModal onRequestClose={this.handleClose} className="modal-outer" isOpen={this.props.isOpen} shouldCloseOnEsc={true} ariaHideApp={false} >
                <div className="modal-inner">
                    <h3>Delete Dashboard?</h3>
                    <div className="d-flex flex-row justify-content-center">
                        <button onClick={this.handleDelete} className="btn_orange">Delete!</button>
                        <button onClick={this.handleClose} className="btn_clear">No</button>
                    </div>
                </div>
            </ReactModal >
        )
    }
}

export default DeleteDashModal;