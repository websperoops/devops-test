import React from 'react'
import ShipstationIntegrationModal from './ShipstationIntegrationModal';
import StatusSpinner from './StatusSpinner';
import IntegrationMenu from './IntegrationMenu';
import IntegrationDisconnectModal from './IntegrationDisconnectModal';
import IntegrationModal from './IntegrationModal';
import IntegrationServiceBlock from './IntegrationServiceBlock';
import AddIntegrationServiceBlock from './AddIntegrationServiceBlock';
import './integrations.css';

class IntegrationServices extends React.Component {
    /*state = {
        showIntegrationModal: false,
      }*/
    constructor(props) {
        super(props);
        this.state = {
            added_ints: added_integrations,
            not_added_ints: not_added_integrations,
            logo_images: logo_images,
            connect_urls: connect_urls,
            showDeleteModal: false,
            selectedTitle: null,
            showStatusSpinner: false,
            statusMessage: '',
            status: '',
            showShipstationModal: false
        };
    }

    componentDidMount() {
        this.setState({ showIntegrationModal: googleInfoNeeded })

        this.state.added_ints.map(int => {
            this.getStatusSync(int)
        })

        if (window.location.href.indexOf('?shop=') > -1 && window.location.href.indexOf('&process=connect') > -1) { //on facebook redirect redirect back to /dashboards/integrations
            window.location.href = '/dashboards/integrations/'
        }

    }

    getStatusJson = async (name) => {
        const res = await fetch(`../integration_sync_status/?name=${name}`)
        const json = res.json();

        return json

        // else {
        //     window.location.href = `${window.location.origin}/dashboards/integrations/`
        // }
    }

    getStatusSync = async (name) => {


        const json = await this.getStatusJson(name);

       


        if (json.status === 'FAILURE') {
            this.setState({
                status: json.status
            })
            this.setState({ showStatusSpinner: true })
            this.setState({ statusMessage: `Failed to sync the following integration: ${name}` })
        }
        else if (json.status === 'PENDING') {
            //If Pending do nothing?
        }
        else if (json.status !== 'SUCCESS') { //If its not finished syncing data show the spinner
            this.setState({ showStatusSpinner: true })
           
            this.setState({ statusMessage: `Please wait while we sync ${name}` })
            setInterval(async () => {
                const waitJson = await this.getStatusJson(name);
                if (waitJson.status === 'SUCCESS') {
                    this.setState({
                        status: waitJson.status,
                        showStatusSpinner: false
                    })

                }

            }, 5000)

        }

    }

    closeStatusModal = () => {
        this.setState({ showStatusSpinner: false })
    }

    ToggleIntegrationModal = () => {
        this.setState((state, props) => ({
            showIntegrationModal: !state.showIntegrationModal
        }));
       
    }

    ToggleDeleteModal = (title) => {
        this.setState((state, props) => ({
            showDeleteModal: !state.showDeleteModal,
            selectedTitle: title
        }));
    }

    handleHideDeleteModal = () => {
        this.setState({ showDeleteModal: false })
    }

    closeShipstationModal = () => this.setState({ showShipstationModal: false })
    openShipstationModal = () => this.setState({ showShipstationModal: true })
    render() {
        let ints = this.state.added_ints
        return (
            <div>
                <div className="spinner-border" role="status">
                    <span className="sr-only">Loading...</span>
                </div>
                <ShipstationIntegrationModal closeModal={this.closeShipstationModal} showModal={this.state.showShipstationModal} />
                <StatusSpinner msg={this.state.statusMessage} status={this.state.status} show={this.state.showStatusSpinner} closeStatusModal={this.closeStatusModal} failure={this.state.status === "FAILURE"} />
                <IntegrationMenu ToggleIntegrationModal={this.ToggleIntegrationModal} />
                <IntegrationDisconnectModal handleHideDeleteModal={this.handleHideDeleteModal}
                    ToggleDeleteModal={this.ToggleDeleteModal} title={this.state.selectedTitle}
                    showDeleteModal={this.state.showDeleteModal} />

                {this.state.showIntegrationModal ? <IntegrationModal
                    ToggleIntegrationModal={this.ToggleIntegrationModal}
                    not_added_ints={this.state.not_added_ints}
                    logo_images={this.state.logo_images}
                    connect_urls={this.state.connect_urls}
                    openShipstationModal={this.openShipstationModal}

                /> : null}
                <div className="integration_services_container">
                    {this.state.added_ints.map((ints, index) => {
                        return (
                            <IntegrationServiceBlock
                                title={ints.name}
                                email={ints.email}
                                other={ints.other}
                                data={ints.data}
                                count={ints.count}
                                img={this.state.logo_images[ints.name]}
                                key={index}
                                ToggleDeleteModal={this.ToggleDeleteModal}
                            />
                        )
                    })}
                    <AddIntegrationServiceBlock ToggleIntegrationModal={this.ToggleIntegrationModal} />
                </div>
            </div>
        )
    }

}

export default IntegrationServices;
