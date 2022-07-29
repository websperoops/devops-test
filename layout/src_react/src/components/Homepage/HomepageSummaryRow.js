import React, { Component } from 'react';
import { getIntegrationsList, getSummaryIntegrationsList, getSummaryMetricData, getSummaryTimeRange, getUserProfile, getUserInfo} from '../../api/BLApi';
import { Button, Modal } from 'react-bootstrap';
import HomepageSummary from './HomePageSummary';
import _ from 'lodash'
import HomepageHeaderDropdown from './HomepageHeaderDropdown';
import './summaryMetrics.css'; 

class HomepageSummaryRow extends Component {

    constructor(props) {
        super(props)
        this.state = {
            metricProps: [],
            time : 'Past 3 Months',
            timeOption : [],
            loading : true,
            dates: false,
            completedTasks:{},
            show: false,
            user: {}
        }
    }

    componentDidMount() {
        getUserProfile().then(data => {
            this.setState({
                user: data.results[0]
            })
            this.setState({
              completedTasks: {
                "has_integrated_social_account": data.results[0].has_integrated_social_account,
                "has_visited_dashboard" : data.results[0].has_visited_dashboard,
                "has_completed_profile" : data.results[0].has_completed_profile,
            }
            })
        })

        getUserInfo().then (data=>{
            let userarr=data.results[0]
            let dateJoined= new Date(userarr.date_joined)
            let defaultDate=new Date('2020-12-25');
            if(dateJoined<defaultDate){
                this.setState({
                  dates: false
                })
            }else{
              this.setState({
                dates: true
              })
            }
        })

        // Get integrations list and determine which metrics to show
        Promise.all([getSummaryMetricData(), getIntegrationsList(), getSummaryIntegrationsList()]).then(res => {
            const summaryMetricsInfo = res[0].results 
            let list = []
            let integrations = []

            // match integration priority and integration id into integrations list
            for(let i=0; i<res[1].length; i++) {
                for(let j=0; j<res[2].length; j++) {
                    if(res[1][i].name === res[2][j].name) {
                        integrations.push({...res[1][i], integration_id: res[2][j].id, priority_number: res[2][j].priority_number})
                        break
                    }
                }
            }

            // sort integrations by priority
            integrations = integrations.sort((a, b) => {
                const integration1 = a.priority_number
                const integration2 = b.priority_number

                if(integration1 > integration2) return 1
                if(integration1 < integration2) return -1

                return 0
            })

            // determine which metrics to show based on the number of integratons
            if(integrations.length >= 4) {
                const selectedIntegrations = integrations.slice(0, 4)

                selectedIntegrations.forEach(integration => {
                    for(let i=0; i<summaryMetricsInfo.length; i++) {
                        if(summaryMetricsInfo[i].integration === integration.integration_id && summaryMetricsInfo[i].metric_priority === 1) {
                            list.push({...summaryMetricsInfo[i], integration_name: integration.name})
                        }
                    }
                })
            } else if (integrations.length === 3) {
                integrations.forEach(integration => {
                    for(let i=0; i<summaryMetricsInfo.length; i++) {
                        if(integration.priority_number === 1) {
                            if(summaryMetricsInfo[i].integration === integration.integration_id && summaryMetricsInfo[i].metric_priority === 1 || summaryMetricsInfo[i].integration === integration.integration_id && summaryMetricsInfo[i].metric_priority === 2) {
                                list.push({...summaryMetricsInfo[i], integration_name: integration.name})
                            }
                        } else {
                            if(summaryMetricsInfo[i].integration === integration.integration_id && summaryMetricsInfo[i].metric_priority === 1) {
                                list.push({...summaryMetricsInfo[i], integration_name: integration.name})
                            }
                        }
                    }
                })
            } else if (integrations.length === 2) {
                integrations.forEach(integration => {
                    for(let i=0; i<summaryMetricsInfo.length; i++) {
                        if(summaryMetricsInfo[i].integration === integration.integration_id && summaryMetricsInfo[i].metric_priority === 1 || summaryMetricsInfo[i].integration === integration.integration_id && summaryMetricsInfo[i].metric_priority === 2) {
                            list.push({...summaryMetricsInfo[i], integration_name: integration.name})
                        }
                    }
                })
            } else if (integrations.length === 1) {
                integrations.forEach(integration => {
                    for(let i=0; i<summaryMetricsInfo.length; i++) {
                        if(summaryMetricsInfo[i].integration === integration.integration_id) {
                            list.push({...summaryMetricsInfo[i], integration_name: integration.name})
                        }
                    }
                })
            }

            this.setState({ metricProps: list })

            // getSummaryTimeRange
            getSummaryTimeRange().then(res => {
                let options = res.map(r => {
                    if(r.name === 'Past Year') return {...r, compare_until: 'now%5C-2y'}
                    else return r
                })

                this.setState({ timeOption : options})
                this.setState({ loading : false})
            })
        })
    }

    handleShow=()=>{
        this.setState({ show: true })
    }

    handleClose=()=>{
        this.setState({ show: false})
    }

    render() {
        let {completedTasks, show, user} = this.state
        return (
            <>
                <div className='d-flex flex-wrap' id='summary-container-id'>
                {Object.values(completedTasks).filter(x => x).length<Object.keys(completedTasks).length && this.state.dates===true ?
                    <div className="homepage-onboarding-btn"> 
                      <span className="homepage-onboarding-header" style={{color: "#8D8D8D"}}>My Onboarding Checklist : </span>
                      <Button
                        className="checklist_button"
                        onClick={this.handleShow}
                      >
                        <i className="far fa-check-circle" style={{fontFamily: "fontawesome", marginRight:"1rem"}}></i>
                        {Object.values(completedTasks).filter(x => x).length}/{Object.keys(completedTasks).length}
                      </Button>
                    </div>:
                    <></>
                }

                <Modal
                    show={show}
                    onHide={this.handleClose}
                    backdrop="static"
                    keyboard={false}
                    style={{padding: "0"}}
                    className="checklist_modal"
                >
                    <Modal.Header >
                        <Modal.Title style={{color: 'black'}}>My Onboarding Checklist</Modal.Title>
                    </Modal.Header>
                    <Modal.Body className="onboarding-cards">
                        <div className="row"> 
                            <div className="col-md-12">
                                <div className="accounts_container">
                                    <ul className="check_list" style={{overflowY: "hidden", width: "100%", height:"100%"}}>                    
                                        <li  className="check_list_item" style={{height: "auto", width: "100%"}}  onClick={()=>{ window.location.href="/dashboards/integrations/"}}>
                                            <img className="integration_modal_logo" src='../../../../static/images/link_icon.svg' alt="" />
                                            <div style={{marginLeft: '3em'}} className="d-flex flex-column">
                                                <p className="checklist_item_name" style={{minWidth: "164.55px"}}>Add an integration</p>
                                            </div>
                                            <div style={{textAlign: "right"}}>
                                                {user.has_integrated_social_account ? 
                                                    <>
                                                        <img style={{top: '12px'}}  src='../../../../static/images/check-circle.svg' alt="completed icon" />
                                                    </>
                                                    :
                                                    <>
                                                        <img style={{top: '12px'}}  src='../../../../static/images/emptycheck-circle.svg' alt="pending icon" />
                                                    </>
                                                }
                                            </div>
                                        </li>

                                        <hr style={{width: "75%"}} />

                                        <li  className="check_list_item" style={{height: "auto", width: "100%"}}  onClick={()=>{ window.location.href="/dashboards/v2/"}}>
                                            <img  className="integration_modal_logo" src='../../../../static/images/dashboard_icon.svg' alt="" />
                                            <div style={{marginLeft: '3em'}} className="d-flex flex-column">
                                                <p className="checklist_item_name">Visit your Dashboards</p>
                                            </div>
                                            <div style={{textAlign: "right"}}>
                                                {user.has_visited_dashboard ?
                                                    <>
                                                        <img style={{top: '12px'}}  src='../../../../static/images/check-circle.svg' alt="completed icon" />
                                                    </>
                                                    :
                                                    <>
                                                        <img style={{top: '12px'}}  src='../../../../static/images/emptycheck-circle.svg' alt="pending icon" />
                                                    </>
                                                }
                                            </div>
                                        </li>

                                        <hr style={{width: "75%"}}/>

                                        <li  className="check_list_item" style={{height: "auto", width: "100%"}}  onClick={()=>{ window.location.href="/dashboards/profile/"}}>
                                            <img className="integration_modal_logo" src='../../../../static/images/profile_icon.svg' alt="" />
                                            <div style={{marginLeft: '3em'}} className="d-flex flex-column">
                                                <p className="checklist_item_name">Complete your Profile</p>
                                            </div>
                                            <div style={{textAlign: "right"}}>
                                                {user.has_completed_profile ?
                                                    <>
                                                        <img style={{top: '12px'}}  src='../../../../static/images/check-circle.svg' alt="completed icon" />
                                                    </>
                                                    :
                                                    <>
                                                        <img style={{top: '12px'}}  src='../../../../static/images/emptycheck-circle.svg' alt="pending icon" />
                                                    </>
                                                }
                                            </div>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </Modal.Body>
                    <Modal.Footer style={{justifyContent:"center"}}>
                        <Button className="grey_button" onClick={this.handleClose}>
                            Close
                        </Button>
                    </Modal.Footer>
                </Modal>

                {!this.state.loading && 
                    <HomepageHeaderDropdown
                    time={this.state.time}
                    selectTime={(t) => this.setState({ time : (t)})}
                    options={this.state.timeOption.map(option => option.name)}
                    type={'summary-metrics'}
                    />
                }  

                {
                    !this.state.loading &&
                    (this.state.metricProps.length ? this.state.metricProps.map((mp, i) => (
                        <HomepageSummary key={i} metricProps={mp} timeOption={this.state.timeOption} time={this.state.time} id={i}/>
                    )) : <h1>No summary metrics available</h1>)
                }
                </div>
           </>
        )
    }
}

export default HomepageSummaryRow;
