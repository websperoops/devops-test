import React, { useState } from 'react';
import ReactModal from 'react-modal';
import { Alert } from 'react-bootstrap';
import './ReauthModal.css';

const ReauthModal = ({ reauthIntegrations }) => {
  let connect_urls = {
    google: '/google/login/?process=connect',
    facebook: '/facebook/login/?process=connect',
    instagram: '/facebook/login/?process=connect',
    quickbooks: '/quickbooks/login/?process=connect',
    mailchimp: '/mailchimp/login/?process=connect',
    shopify: '/dashboards/integrate/shopify',
    twitter: '/twitter/login/?process=connect',
    etsy: '/etsy/login/?process=connect',
    woocommerce: '/etsy/login/?process=connect',
  };

  const [showModal, setShowModal] = useState(true);
  const [reauthUrl, setReauthUrl] = useState('');

  const openModal = () => {
    setShowModal(true);
  };

  const closeModal = () => {
    alert('Please reauthenticate your accounts!');
    setShowModal(false);
  };

  const onClick = (e, store) => {
    if(store) setReauthUrl(connect_urls[e.target.id] + '/' + store);
    else setReauthUrl(connect_urls[e.target.id]);
  };

  const renderList = () => {
    return reauthIntegrations.map((integration, idx) => (
      <>
        <div className="reauth-selection-row" key={integration.provider}>
          <div className="reauth-selection">
            <div className="img-container">
              <img className="integration-img" src={`../../../../../static/images/${integration.provider}-icon.png`}/>
            </div>

            <p className="selection-text">
              {integration.provider.slice(0, 1).toUpperCase() + integration.provider.slice(1)}
            </p>

            {
              integration.provider !== 'shopify' ?
              <input
                type="radio"
                name="formHorizontalRadios"
                id={integration.provider}
                onClick={onClick}
              /> :
              <div style={{width: '13px' }}></div>
            }
          </div>
        </div>
        {
          integration.provider === 'shopify' && (
            integration.stores.map((store, idx2) => (
              <>
                <div className={`reauth-store-row ${idx2 < integration.stores.length - 1 && 'reauth-store-row-bottom-line'}`}>
                  <div>{store}</div>
                  <input
                    type="radio"
                    name="formHorizontalRadios"
                    id={integration.provider}
                    onClick={e => onClick(e, store)}
                  />
                </div>
                {idx < reauthIntegrations.length - 1 && idx2 === integration.stores.length - 1 && <div className="selection-divider"></div>}
              </>
            )
          )
          )
        }
      </>
    ));
  };


  return (
    <>
      {reauthIntegrations.length > 0 && (
        <Alert className="reauth-message" onClick={openModal} variant="danger">
          Click here to reauthenticate your accounts.
        </Alert>
      )}

      <ReactModal
        ariaHideApp={false}
        onRequestClose={closeModal}
        className="reauth-modal-container"
        isOpen={showModal}
        shouldCloseOnEsc={true}
        shouldCloseOnOverlayClick={true}
      >
        <h3 className="reauth-header">We're Sorry!</h3>

        <div className="reauth-box">
          <img src="../../../../../static/svg/alldatainoneplace.svg" style={{ width: '50px', marginBottom: '20px' }}/>

          <div>
            <p style={{ marginBottom: '9px' }}>There was an error syncing these accounts.{' '}</p>
            <p style={{ marginBottom: '20px' }}>Please reauthenticate.</p>
          </div>

          <form className="reauth-selections-container">{renderList()}</form>
        </div>

        <div className="reauth-btns">
          <a href={reauthUrl} target="_blank">
            <button className="reauth-btn reauth-btns-reauthenticate">Reauthenticate</button>
          </a>
          <button className="reauth-btn reauth-btns-cancel" onClick={closeModal}>Cancel</button>
        </div>
      </ReactModal>
    </>
  );
};

export default ReauthModal;
