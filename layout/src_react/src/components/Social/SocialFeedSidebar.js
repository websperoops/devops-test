import React, { Fragment, useContext } from 'react'
import { SocialData } from './SocialContainer'


function SocialFeedSideBar(props) {
    const { activatePostModal, feedLinkChange } = useContext(SocialData);
    return (
        <Fragment>

            <div className="float-left">
                <div className="social-title">
                    <h3 className="social-header bottom_orange">Social</h3>
                </div>
                <div className="social-sidebar">
                    <div className="social_btn_container text-center mr-3">
                        <button onClick={activatePostModal} className="btn_orange" style={{ width: '100px' }}>Create A Post</button>
                    </div>
                    <button onClick={activatePostModal} className="btn_orange mobile-social-btn"><i className="fa fa-plus text-center"></i></button>
                    <ul className="sidebar-list">
                        <li className="bottom_orange" style={{ width: '85px' }}><a href="#">My Inbox</a></li>
                        <li onClick={() => feedLinkChange('All Activity')}><a href="#">All Activity</a></li>
                        <li onClick={() => feedLinkChange('Conversations')}><a href="#">Conversations</a></li>
                        <li onClick={() => feedLinkChange('Interactions')}><a href="#">Interactions</a></li>
                        <li onClick={() => feedLinkChange('Follows')}><a href="#">Follows</a></li>
                    </ul>
                </div>
            </div>
        </Fragment>
    )
}

export default SocialFeedSideBar