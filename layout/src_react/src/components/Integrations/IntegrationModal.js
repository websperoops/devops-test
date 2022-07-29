import React, { Fragment } from 'react'
import GoogleAnalyticsModal from './GoogleAnalyticsModal'
import './integrations.css';

class IntegrationModal extends React.Component {

    state = {
        showGoogleModal: false,
    }

    componentDidMount() {
        if (googleInfoNeeded) {
            this.setState({ showGoogleModal: true })
        }

    }

    checkIntegration = (name, e) => {
        if (name === 'shipstation') {
            this.props.openShipstationModal()
            this.props.ToggleIntegrationModal()
        }
    }


    checkIfAvailable = (name) => {

        return true;
    }


    closeGoogleModal = () => this.setState({ showGoogleModal: false });

    render() {
        let { ToggleIntegrationModal, not_added_ints, logo_images, connect_urls } = this.props;
        return (<Fragment>
            <div className="integration_modal">
                <div className="integration_modal_container">

                    <h4>Select An Account </h4>

                    <div className="integration_modal_input_container">
                        <label htmlFor="search_account" className="search_account_label">Search</label>
                        <input type="text" name="search_account" className="search_account_input" />
                        <i className="fa fa-search"></i>
                    </div>

                    <div className="accounts_container">
                        <ul className="accounts_list">
                            {not_added_ints.map((int, index) => (
                                <li key={index} className="account_list_item" style={int === 'etsy' ? {height:'120px'} : {height: 'auto'}}>
                                    <img style={{top: '12px',width: '40px',position: 'absolute',left: '-10px'}} className="integration_modal_logo" src={logo_images[int]}
                                        alt={`${int}_logo`} />
                                        <div style={int == 'twitter' ? {marginLeft: '-20px'} : null} className="d-flex flex-column">
                                    <p style={int === 'etsy' ? {marginLeft:'-75px'} : null} className="integration_modal_item_name">{int}</p>
                                    {int == 'etsy' && <p className="text-left etsy-ps">
                                    The term 'Etsy' is a trademark of Etsy, Inc. This application uses the Etsy API 
                                    but is not endorsed or certified by Etsy, Inc.    
                                    </p>}
                                    </div>

                                    {this.checkIfAvailable(int) ?
                                        <a onClick={(e) => this.checkIntegration(int, e)} href={connect_urls[int]}>
                                            <button className='btn_connect account_item_btn'>Connect</button>
                                        </a>
                                        :
                                        <a onClick={(e) => e.preventDefault()}>
                                            <button
                                                className='light_gray_btn account_item_btn'>Coming Soon
                                                </button>
                                        </a>
                                    }
                                </li>

                            ))
                            }
                        </ul>
                    </div>
                    <div className="integration_modal_buttons">
                        <button onClick={() => ToggleIntegrationModal()} className="btn_cancel">Cancel</button>
                    </div>
                </div>
            </div>
            {this.state.showGoogleModal ? <GoogleAnalyticsModal closeGoogleModal={this.closeGoogleModal} /> : null}

        </Fragment>
        )
    }

};

export default IntegrationModal;