import React from 'react'
import { Button,Modal,Card } from 'react-bootstrap';
import {getUserProfile,getUserInfo} from "../../api/BLApi";
import './integrationMenu_integrationServiceBlock.css';


class IntegrationMenu extends React.Component {
    state = {
        addNewIntegration: false,
    }
    constructor(props) {
        super(props);
        this.state = {
          user:{},
          show: false,
          checklist_count: 3,
          dates: false,
          completedTasks:{}
        };
      }
componentDidMount=()=>{
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
}
handleClose=()=>{
    this.setState({
        show: false
    })
}
handleShow=()=>{
    this.setState({
        show: true
    })
}
    render() {
        let user=this.state.user
        let show=this.state.show
        let completedTasks=this.state.completedTasks
        return (
            <>
            <div className="integration_menu" >
                <div className="integration_menu_title">
                    <h3 className="integration_menu_header ">My Integrations</h3>
                </div>
                <div style={{textAlign: "right"}}>
                  {Object.values(completedTasks).filter(x => x).length<Object.keys(completedTasks).length && this.state.dates===true ?
                    <div>
                      <span className="onboarding-header">My Onboarding Checklist : </span>
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
                </div>
            </div>
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
                           
                                <li  className="check_list_item" style={{height: "auto", width: "100%"}} onClick={()=>{ window.location.href="/dashboards/integrations/"}}>
                                    <img className="integration_modal_logo" src='../../../../static/images/link_icon.svg'
                                        alt="" />
                                        <div 
                                       style={{marginLeft: '3em'}}
                                         className="d-flex flex-column">
                                    <p className="checklist_item_name" style={{minWidth: "164.55px"}}>Add an integration</p>
                                    </div>
                                      <div style={{textAlign: "right"}}>
                                      {user.has_integrated_social_account ? <>
                                            <img style={{top: '12px'}}  src='../../../../static/images/check-circle.svg'
                                        alt="completed icon" />
                                          </>:<>
                                          <img style={{top: '12px'}}  src='../../../../static/images/emptycheck-circle.svg'
                                        alt="pending icon" />
                                          </>}
                                      </div>
                                </li>
                                <hr style={{width: "75%"}} />
                                <li  className="check_list_item" style={{height: "auto", width: "100%"}}  onClick={()=>{ window.location.href="/dashboards/v2/"}}>
                                    <img className="integration_modal_logo" src='../../../../static/images/dashboard_icon.svg'
                                        alt="" />
                                        <div
                                       style={{marginLeft: '3em'}}
                                         className="d-flex flex-column">
                                    <p className="checklist_item_name">Visit your Dashboards</p>
                                    </div>
                                    <div style={{textAlign: "right"}}>
                                    {user.has_visited_dashboard ? <>
                                            <img style={{top: '12px'}}  src='../../../../static/images/check-circle.svg'
                                        alt="completed icon" />
                                          </>:<>
                                          <img style={{top: '12px'}}  src='../../../../static/images/emptycheck-circle.svg'
                                        alt="pending icon" />
                                          </>}
                                      </div>
                                </li>
                                <hr style={{width: "75%"}}/>
                                <li  className="check_list_item" style={{height: "auto", width: "100%"}}  onClick={()=>{ window.location.href="/dashboards/profile/"}}>
                                    <img  className="integration_modal_logo" src='../../../../static/images/profile_icon.svg'
                                        alt="" />
                                        <div 
                                       style={{marginLeft: '3em'}}
                                         className="d-flex flex-column">
                                    <p className="checklist_item_name">Complete your Profile</p>
                                    </div>
                                    <div style={{textAlign: "right"}}>
                                    {user.has_completed_profile ? <>
                                            <img style={{top: '12px'}}  src='../../../../static/images/check-circle.svg'
                                        alt="completed icon" />
                                          </>:<>
                                          <img style={{top: '12px'}}  src='../../../../static/images/emptycheck-circle.svg'
                                        alt="pending icon" />
                                          </>}
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
            </>
        )
    }
}

export default IntegrationMenu;
