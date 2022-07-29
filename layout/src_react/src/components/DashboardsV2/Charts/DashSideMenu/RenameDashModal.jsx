import React, { Component } from 'react'
import ReactModal from 'react-modal';
import { renameDashboard } from '../../../../api/BLApi';

class RenameDashModal extends Component {

    constructor(props) {
        super(props)
        this.state = {
            name: props.currentName
        }
        this.handleRename = this.handleRename.bind(this)
        this.handleClose = this.handleClose.bind(this)
        this.handleOnEnter = this.handleOnEnter.bind(this)
    }

    handleClose() {
        this.props.closeFunc()
    }

    handleRename() {
        this.state.name.length && renameDashboard(this.state.name, this.props.dashboardId).then(data => {
            this.state.name.length && this.props.renameDash(this.state.name)
            this.props._loadDashboardList() //after renaming, refresh the dashboardList from api and get new list including the renamed dashboard.
            this.props.closeFunc()
        }).catch((err) => { console.error(err) })

    }

    handleOnEnter(e) {
        if (e.charCode === 13) {
            this.handleRename()
        }
    }

    render() {
        return (
            <ReactModal ariaHideApp={false} onRequestClose={this.handleClose} shouldCloseOnEsc={true} isOpen={this.props.isOpen} className="modal-outer" >
                <div className="modal-inner">
                    <h3 className="mb-3">Rename Dashboard</h3>
                    <input onKeyPress={this.handleOnEnter} className="text-center" type="text" value={this.state.name} onChange={e => this.setState({ name: e.target.value })} placeholder="New Name" style={{ border: '1px solid #ddd', borderRadius: '10px', width: '300px' }} />
                    <div className="d-flex flex-row justify-content-center">
                        <button disabled={this.state.name ? !this.state.name.length : true} className={this.state.name ? !this.state.name.length ? 'btn_gray' : 'btn_orange' : 'btn-gray'} onClick={this.handleRename}>Rename!</button>
                        <button onClick={this.handleClose} className="btn_clear">Cancel</button>
                    </div>

                </div>
            </ReactModal>
        )
    }
}

export default RenameDashModal;