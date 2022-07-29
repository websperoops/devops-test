import React, { Fragment, useContext } from 'react'
import { SocialData } from './SocialContainer'

function SocialPublishSideBar() {
    const { publishLinkChange } = useContext(SocialData);
    return (
        <Fragment>
            <div className="float-left">
                <div className="social-title">
                    <h3 className="social-header bottom_orange">Social</h3>
                </div>
                <div className="social-sidebar">
                    <div className="social_btn_container text-center mr-3">
                        <button className="btn_orange" style={{ width: '100px' }}>Create A Post</button>
                    </div>
                    <ul className="sidebar-list">
                        <li onClick={() => publishLinkChange('My History')}><a href="#">My History</a></li>
                        <li onClick={() => publishLinkChange('Schedule')}><a href="#">Schedule</a></li>
                        <li onClick={() => publishLinkChange('Drafts')}><a href="#">Drafts</a></li>
                    </ul>
                </div>
            </div>
        </Fragment>
    )
}

export default SocialPublishSideBar