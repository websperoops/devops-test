import React from 'react'
import ReactModal from 'react-modal';

function DashDeleteModal(props) {
    const deleteDash = () => {
        window.location.href = '../../delete';
    }

    const close = () => props.close();

    return (
        <ReactModal onRequestClose={close} className="modal-outer" isOpen={props.show} shouldCloseOnEsc={true} ariaHideApp={false}>
            <div className="modal-inner">
                <h3>Delete Dashboard?</h3>

                <div className="d-flex flex-row justify-content-center">
                    <button onClick={deleteDash} className="btn_orange">Delete!</button>
                    <button onClick={close} className="btn_clear">No</button>
                </div>
            </div>
        </ReactModal>
    )
}

export default DashDeleteModal;