import React, { Component } from 'react'
import { addDashboard } from '../../../../api/BLApi'
import ReactModal from 'react-modal';

class NewDashModal extends Component {

    constructor(props) {
        super(props);
        this.state = {
            name: '',
        }
        this.handleClose = this.handleClose.bind(this)
        this.handleCreateDash = this.handleCreateDash.bind(this)
        this.handleOnEnter = this.handleOnEnter.bind(this)
    }

    handleClose() {
        this.props.closeFunc()
    }

    handleCreateDash() {
        addDashboard({ name: this.state.name, user: this.props.userId }).then(data => {
            window.location.href = `${window.location.origin}/dashboards/v2/${data.id}`
            this.handleClose()
        }).catch((err) => { console.error(err) })
    }

    handleOnEnter(e) {
        if (e.charCode === 13) {
            this.handleCreateDash()
        }
    }

    render() {
        return (
            <ReactModal onRequestClose={this.handleClose} isOpen={this.props.isOpen} shouldCloseOnEsc={true} shouldCloseOnOverlayClick={true} ariaHideApp={false} className="modal-outer">
                <div className="modal-inner">
                    <h3>Add New Dashboard</h3>
                    <div className=" mt-4 d-flex flex-column justify-content-center bg-light">
                        <div className="d-flex flex-column justify-content-center mt-3">
                            <label html="dash-name" style={{ fontSize: '20px' }}>Dashboard Title</label>
                            <input onKeyPress={this.handleOnEnter} id="dash-name" className="mx-auto" type="text" onChange={e => this.setState({ name: e.target.value })} style={{ width: '300px', borderRadius: '10px', border: '1px solid #ddd', textAlign: 'center' }} />
                        </div>
                        <div className="d-flex flex-row justify-content-center">
                            <button onClick={this.handleCreateDash} disabled={!this.state.name.length} className={!this.state.name.length ? 'btn_gray' : 'btn_orange'}>Create!</button>
                            <button onClick={this.handleClose} className="btn_clear">Cancel</button>
                        </div>
                    </div>
                </div>
            </ReactModal>
        )
    }
}

export default NewDashModal;