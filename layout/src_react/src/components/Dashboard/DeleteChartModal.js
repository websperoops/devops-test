import React, { useEffect } from 'react'
import ReactModal from 'react-modal'


function DeleteChartModal(props) {
    const deleteIt = () => {
        fetch(`/dashboards/remove_chart/?slug=${props.id}`);
        $(`#${props.id}_container`).remove();
        close();
    }
    const close = () => props.close();

    return (
        <ReactModal onRequestClose={close} className="modal-outer" isOpen={props.show} shouldCloseOnEsc={true} shouldCloseOnOverlayClick={true} ariaHideApp={false}>
            <div className="modal-inner">
                <h3 style={{ fontSize: '20px' }}>Delete this Metric?</h3>
                <div className="d-flex flex-row justify-content-center">
                    <button onClick={deleteIt} className="btn_orange">Yes</button>
                    <button onClick={close} className="btn_clear">No</button>
                </div>
            </div>
        </ReactModal>
    )
}

export default DeleteChartModal;