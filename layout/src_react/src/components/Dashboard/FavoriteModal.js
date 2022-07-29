import React, { useEffect } from 'react'
import ReactModal from 'react-modal'


function FavoriteModal(props) {
    const faveIt = () => {
        fetch(`/dashboards/add_chart_to_favorites/?chart_id=${props.id}`);
        close();
    }
    const close = () => props.close();

    return (
        <ReactModal onRequestClose={close} className="modal-outer" isOpen={props.show} shouldCloseOnEsc={true} shouldCloseOnOverlayClick={true} ariaHideApp={false}>
            <div className="modal-inner">
                <h3 style={{ fontSize: '20px' }}>Favorite this Metric?</h3>
                <div className="d-flex flex-row justify-content-center">
                    <button onClick={faveIt} className="btn_orange">Yes</button>
                    <button onClick={close} className="btn_clear">No</button>
                </div>
            </div>
        </ReactModal>
    )
}

export default FavoriteModal;