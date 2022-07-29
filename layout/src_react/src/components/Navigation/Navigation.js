import React, { useState, useEffect} from 'react'
import {Form} from 'react-bootstrap'
import axios from 'axios';
function Navigation  () {
    const [allShops, setAllShops] = useState([]);
    const [currentShop, setCurrentShop] = useState({});
    const [selectedShop, setSelectedShop] = useState({});
    const [hideSelect, setHideSelect]= useState(true)
    const toggleShop=(evt)=>{
        setSelectedShop(evt.target.value)
        axios.get(`/dashboards/shopify/toggle/?id=${evt.target.value}`).then(()=>window.location.reload() )
    }
    useEffect(() => {
      axios.get('/dashboards/shopify/shop_id').then(res=>{
          setAllShops(res.data);
         
            if(res.data.length>0){
                setHideSelect(false)
                res.data.map((val, index)=>{
                    if(val["is_selected"]===true){
                        
                        setCurrentShop(val)
                        setSelectedShop(val.shop_id)
                    }
                })
            }else{
                setHideSelect(true)
            }
      } 
      )
    }, [])
    return (
        <div className="topbar">
            <div className="topbar-left d-flex">
                <div className="text-center ml-3">
                    <a href="/" className="logo"><img className="topbar-logo" src="/static/images/BlocklightLogo_Full_Transparent_WhiteText.svg"
                       /></a>
                </div>
    
            </div>
    
    
            <nav className="navbar-custom dark-theme-nav-bar">
    
    
                <ul className="list-inline float-left mb-0 left-menu">
                    <li className="list-inline-item">
                        <a href="/dashboards/homepage" className="waves-effect waves-primary nav-link menu-item">
                            <img src="/static/svg/Home_Icon.svg" className="nav-icon" />
                            <span>Homepage</span></a>
                    </li>
    
    
                    <li className="list-inline-item">
                        <a href="/dashboards/v2" className="waves-effect waves-primary nav-link menu-item">
                            <img src="/static/svg/Dashboards_Icon.svg" className="nav-icon" /><span>Dashboards</span></a>
                    </li>
    
                    <li className="list-inline-item">
                        <a href="/dashboards/integrations" className="waves-effect waves-primary nav-link menu-item">
                            <img src="/static/svg/Integrations_Icon.svg" className="nav-icon" /><span>Integrations</span></a>
                    </li>
    
                    <li className="list-inline-item">
    
                        <a href="/dashboards/social" className="waves-effect waves-primary nav-link menu-item">
                            <img src="/static/svg/Social_Icon.svg" className="nav-icon" /> <span>Social</span></a>
                    </li>
    
                </ul>
                <div className="hide-phone dropdown collapsed-list list-inline float-left">
                    <a className="nav-link dropdown-toggle waves-effect waves-light nav-user" data-toggle="dropdown" href="#"
                        role="button" aria-haspopup="false" aria-expanded="false">
                        <i className="ti-menu"></i>
                    </a>
                    <div className="dropdown-menu dropdown-menu-right sections-dropdown " aria-labelledby="Preview">
                        <a href="/dashboards/homepage" className="d-flex justify-content-center">Homepage</a>
                        <a href="/dashboards/v2" className="d-flex justify-content-center">Dashboards</a>
                        <a href="/dashboards/integrations" className="d-flex justify-content-center">Integrations</a>
                        <a href="/dashboards/social" className="d-flex justify-content-center">Social</a>
                    </div>
                </div>
                <ul className="list-inline float-right mb-0 right-menu">
                    <div>
                        {!hideSelect?<>
                            <div className="list-inline-item list-item-form" >
                        <Form>
                            <Form.Group >
                                <Form.Control className="header-select" as="select" style={{ border:"1px solid #8D8D8D",height: "auto"  }} value={selectedShop} onChange={(evt)=>toggleShop(evt)}>
                                    {allShops.map((val, index)=>{
                                        return <option value={val.shop_id}>{val.name}</option>
                                    })}
                                {/* <option value={2388}>All shops</option> */}
                                </Form.Control>
                            </Form.Group>
                        </Form>
                        </div>
                        </>:<></>}
                   
                        <div className="list-inline-item notification-list hide-phone" style={{ display: 'none' }}>
                            <a className="nav-link waves-light waves-effect" href="#" id="btn-settings">
                                <i className="ti-settings noti-icon"></i>
                            </a>
                        </div>

                        <div className="list-inline-item notification-list hide-phone">
                            <a className="nav-link waves-light waves-effect nav-user" href="/dashboards/feedback" id="btn-feedback">
                                <i className="ti-comment-alt noti-icon" style={{ fontSize: '18px' }}></i>
                            </a>
                        </div>
    
                        <li className="list-inline-item dropdown notification-list">
                            <a className="nav-link dropdown-toggle waves-effect waves-light nav-user" data-toggle="dropdown" href="#"
                                role="button" aria-haspopup="false" aria-expanded="false">
                                <i className="ti-user"></i>
                            </a>
                            <div className="dropdown-menu dropdown-menu-right profile-dropdown " aria-labelledby="Preview">
    
                                {/* <div className="dropdown-item noti-title">
                                    <h5 className="text-overflow"><small>Welcome</small> </h5>
                                </div> */}
    
                                <a href="/dashboards/profile" className="dropdown-item notify-item">
                                    <i className="mdi mdi-account-star-variant"></i> <span>Profile</span>
                                </a>
    
                                <a href="/accounts/logout" className="dropdown-item notify-item">
                                    <i className="mdi mdi-logout"></i> <span>Logout</span>
                                </a>
                            </div>
                        </li>

                        <li className="list-inline-item notification-list hide-phone">
                            <a className="nav-link waves-light waves-effect" href="#" id="btn-fullscreen">
                                <i className="mdi mdi-fullscreen noti-icon"></i>
                            </a>
                        </li>
                    </div>
    
                </ul>
            </nav>
        </div>
    
    );

} 

export default Navigation