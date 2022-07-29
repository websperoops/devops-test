import React, { useEffect } from 'react'
import ReactModal from 'react-modal';
import { csrf_token } from '../../functions/dashboard/dashFunctions'
import './integrations.css';

function ShipstationIntegrationModal(props) {
    const closeModal = () => props.closeModal();



    return (
        <ReactModal style={{ zIndex: 3 }} className="modal-outer" shouldCloseOnOverlayClick={true} ariaHideApp={false} isOpen={props.showModal} onRequestClose={closeModal}>

            <div className="modal-inner">
                <div className="modal-header shipstation-modal-header">
                    <i onClick={closeModal} className="fa fa-times fa-2x"></i>
                    <h3 className="mt-3">Shipstation</h3>
                </div>
                <div id="shipstationform">
                    <form className="form" method="POST" action="addshipstation/" autoCapitalize="off" >


                        <input type="hidden" name="csrfmiddlewaretoken" value={csrf_token} />
                        <input id="user_iden" type="hidden" name="user_iden" value="none" />
                        <input id="integration_name" type="hidden" name="integration_name" value="shipstation" />

                        <div className="d-flex flex-column mt-3 w-75 mx-auto">
                            <label htmlFor="api_key">Key</label>
                            <input id="api_key" type="password" name="api_key" maxLength="100" required />
                        </div>
                        <div className="d-flex flex-column mt-3 w-75 mx-auto">
                            <label htmlFor="api_secret">Secret </label>
                            <input id="api_secret" type="password" name="api_secret" maxLength="100" required />
                        </div>
                        <div className="row justify-content-center align-items-center">
                            <button className="btn_orange" type="submit">Submit</button>
                        </div>

                    </form>
                </div>
            </div>

        </ReactModal>
    )
}

export default ShipstationIntegrationModal;