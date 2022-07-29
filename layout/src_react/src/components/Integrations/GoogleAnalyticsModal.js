import React, { useEffect, useState } from 'react';
import './integrations.css';

const GoogleAnalyticsModal = (props) => {

    const [accounts, setAccounts] = useState([])
    const [properties, setProperties] = useState([])
    const [views, setViews] = useState([])
    const [view, setView] = useState()

    const [selectedAccount, setSelectedAccount] = useState();
    const [selectedProperty, setdelegateProperty] = useState();


    useEffect(() => {
        if (googleAccountOptions) {
            setAccounts(googleAccountOptions)
            setSelectedAccount(googleAccountOptions[0].id)

        }
    }, [googleAccountOptions])


    useEffect(() => {
        if (selectedAccount != null) {
            //update the properties and set views to nothing
            let account = accounts.find(acc => acc.id == selectedAccount)
            setProperties(account.web_properties)
            setViews([])
            setdelegateProperty(account.web_properties[0].id)
        }
    }, [selectedAccount])

    useEffect(() => {
        if (selectedProperty != null) {
            let property = properties.find(prop => prop.id == selectedProperty)
            setViews(property.profiles)
            setView(property.profiles[0].view_id)
        }
    }, [selectedProperty])

    return (
        <div className="google-analytics-modal-outer">
            <div className="google-analytics-header">
                {/* <i onClick={props.closeGoogleModal} className="fa fa-arrow-left fa-2x"></i> */}
                <p>Select an Account</p>

                <span className="underline"></span>
            </div>
            <div className="google-analytics-modal-inner">
                <div className="logo-container">
                    <img src='/static/images/google-analytics-logo.png' className="google-analytics-logo"
                        alt="google-analytics-logo" />
                </div>
                <p>We Found You!</p>
                <p>Please select your account details below to get you set up.</p>

                <div className="d-flex flex-column justify-content-center">
                    <div className="input-selector">
                        <label htmlFor="account">Account:</label>
                        <select
                            onChange={e => setSelectedAccount(parseInt(e.target.value))} id="account">
                            <option disabled>Account</option>
                            {accounts.map((account, index) => <option key={index}
                                value={account.id}>{account.name}</option>)}
                        </select>
                    </div>

                    <div className="input-selector">
                        <label htmlFor="propery">Property:</label>
                        <select
                            onChange={e => setdelegateProperty(parseInt(e.target.value))} disabled={!selectedAccount}
                            id="propery">
                            <option disabled>Property</option>
                            {properties.map((propery, index) => <option key={index}
                                value={propery.id}>{propery.name}</option>)}

                        </select>
                    </div>

                    <div className="input-selector">
                        <label htmlFor="view">View:</label>
                        <select disabled={!selectedProperty} onChange={e => setView(e.target.value)} id="view">
                            <option disabled>View</option>
                            {views.map((view, index) => <option key={index} value={view.view_id}>{view.name}</option>)}
                        </select>
                    </div>
                </div>


                <div className="buttons">
                    <button onClick={(e) => {
                        connectGoogle(view)
                    }} className='btn_orange'>Connect
                    </button>
                    <button onClick={props.closeGoogleModal} className="btn_clear">Cancel</button>
                </div>

            </div>


        </div>
    )
}

export default GoogleAnalyticsModal;