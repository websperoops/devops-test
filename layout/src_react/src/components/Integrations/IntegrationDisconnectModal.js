import React, { useState } from 'react'
import ReactModal from 'react-modal';
import './integrations.css';

function IntegrationDisconnectModal(props) {

    const [removed, setRemoved] = useState(null)

    const handleIntRemoval = () => {
        fetch(`/dashboards/remove/${props.title}`).then(res => {
            if (res.status == 200) {
                setRemoved(true)
            }
        });
        setTimeout(function () {
            location.reload()
        }, 2000)
    }

    const closeModal = () => {
        props.handleHideDeleteModal()
    }

    return (

        <ReactModal className="modal-outer" shouldCloseOnOverlayClick={true} onRequestClose={closeModal}
            isOpen={props.showDeleteModal} ariaHideApp={false}>
            <div className="modal-inner">
                {removed === true && <div className="alert alert-success" role="alert">
                    Integration<p className="text-capitalize">{props.title}</p> removed succesfully.
                </div>}
                <div className="modal-header">
                    <p>Remove <span className="text-capitalize">{props.title}</span>?</p>
                </div>

                <div className="buttons" style={{ marginTop: '-10px' }}>
                    <button onClick={handleIntRemoval} className="btn_orange">Yes</button>
                    <button onClick={closeModal} className="btn_clear">No</button>
                </div>
            </div>
        </ReactModal>

    )
}

export default IntegrationDisconnectModal;