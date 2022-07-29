import React, { useContext } from 'react'
import { SocialData } from './SocialContainer'

function SocialReportsSideBar() {
    const { reportsLinkChange } = useContext(SocialData);
    return (
        <div className="float-left">
            <div className="social-title">
                <h3 className="social-header bottom_orange">Social</h3>
            </div>
            <div className="social-sidebar">
                <div className="social_btn_container text-center mr-3">
                    <button className="btn_orange" style={{ width: '100px' }}>Create A Post</button>
                </div>
                <ul className="sidebar-list">
                    <li onClick={() => reportsLinkChange('All Reports')}><a href="#">All Reports</a></li>
                    <li onClick={() => reportsLinkChange('Engagements')}><a href="#">Engagements</a></li>
                    <li onClick={() => reportsLinkChange('Published')}><a href="#">Published</a></li>
                </ul>
            </div>
        </div>
    )
}

export default SocialReportsSideBar