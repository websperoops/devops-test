import React from 'react'
import ReactModal from 'react-modal';
import './integrations.css';

function StatusSpinner(props) {
    const closeModal = () => {
        props.closeStatusModal()
    }

    return (
        <ReactModal className="modal-outer modal-top-0" onRequestClose={closeModal} shouldCloseOnOverlayClick={true} ariaHideApp={false} isOpen={props.show}>
            <div style={{ display: (props.failure) ? 'none' : 'block' }} className="spinner-container mx-auto"> </div>
            <div className="text-center">
                <p className="lead text-light mt-3">{props.msg}</p>
            </div>

            <div style={{ display: (props.failure) ? 'block' : 'none' }}>
                <i className="text-danger fa fa-exclamation-triangle fa-4x"></i>
                <br></br>
                <button onClick={closeModal} className="btn_orange mx-auto mt-3">Close</button>
            </div>
        </ReactModal >
    )
}

export default StatusSpinner;