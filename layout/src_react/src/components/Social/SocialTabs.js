import React, { useContext } from 'react'
import FeedTabSelected from './FeedTabSelected'
import PublishTab from './PublishTab'
import ReportsTab from './ReportsTab'
import { SocialData } from './SocialContainer'

const SocialTabs = () => {
    const { tabChange } = useContext(SocialData);
    return (
        <div className="float-right social-right-container">
            <nav>
                <div className="text-dark nav nav-tabs" id="nav-tab" role="tablist" style={{ width: '95%' }}>
                    <a onClick={() => tabChange('My Feed')} className="text-dark nav-item nav-link active" id="nav-home-tab" data-toggle="tab" href="#nav-feed" role="tab" aria-controls="nav-feed" aria-selected="true">My Feed</a>
                    <a onClick={() => tabChange('Publish')} className="text-dark nav-item nav-link" id="nav-publish-tab" data-toggle="tab" href="#nav-publish" role="tab" aria-controls="nav-publish" aria-selected="false">Publish</a>
                    <a onClick={() => tabChange('Reports')} className="text-dark nav-item nav-link" id="nav-contact-tab" data-toggle="tab" href="#nav-reports" role="tab" aria-controls="nav-reports" aria-selected="false">Reports</a>
                    <a className="text-dark nav-item nav-link" href="/dashboards/profile">Settings</a>
                </div>
            </nav>

            <div className="tab-content" id="nav-tabContent">
                <div className="tab-pane fade show active" id="nav-feed" role="tabpanel" aria-labelledby="nav-feed-tab">
                    <FeedTabSelected />
                </div>
                <div className="tab-pane fade" id="nav-publish" role="tabpanel" aria-labelledby="nav-publish-tab">
                    <PublishTab />
                </div>

                <div className="tab-pane fade" id="nav-reports" role="tabpanel" aria-labelledby="nav-reports-tab">
                    <ReportsTab />
                </div>
            </div>
        </div>
    )
}

export default SocialTabs;