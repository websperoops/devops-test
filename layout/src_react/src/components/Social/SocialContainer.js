import React, { useState, createContext, useContext, useEffect } from 'react'
import SocialFeedSideBar from './SocialFeedSidebar'
import SocialPublishSideBar from './SocialPublishSideBar'
import SocialReportsSideBar from './SocialReportsSideBar'
import PostModal from './PostModal'
import SocialTabs from './SocialTabs'
import TweetPostModal from './TweetPostModal'
export const SocialData = createContext();


const SocialContainer = () => {
    const [selectedTab, setSelectedTab] = useState('My Feed');
    const [feedLink, setFeedLink] = useState('All Activity');
    const [publishLink, setPublishLink] = useState('My History');
    const [reportsLink, setReportsLik] = useState('All Reports');
    const [showPostModal, setShowPostModal] = useState(false);
    const [twitterMentions, setTwitterMentions] = useState(null)




    useEffect(() => {
        getMentions()
    }, [])
    const getMentions = async () => { //Gets Twitter mentions and saves them to the 'twitterMentions' state
        const res = await fetch('/dashboards/social/mentions')
        const json = await res.json()

        setTwitterMentions(json)
    }


    const tabChange = (tab) => setSelectedTab(tab);
    const feedLinkChange = (selectedLink) => setFeedLink(selectedLink);
    const publishLinkChange = (selectedLink) => setPublishLink(selectedLink);
    const reportsLinkChange = (selectedLink) => setReportsLik(selectedLink);
    const activatePostModal = () => setShowPostModal(true);
    const closePostModal = () => setShowPostModal(false);


    const renderTab = () => {
        if (selectedTab === "My Feed") {
            return <SocialFeedSideBar />
        }
        else if (selectedTab === "Publish") {
            return <SocialPublishSideBar />
        }
        else if (selectedTab === "Reports") {
            return <SocialReportsSideBar />
        }
    }



    return (
        <div className="social-container">
            <SocialData.Provider value={{
                selectedTab, feedLink, publishLink, reportsLink, showPostModal, tabChange, feedLinkChange, publishLinkChange, reportsLinkChange, activatePostModal, closePostModal, twitterMentions
            }}>
                <PostModal />
                <TweetPostModal />
                <div className="float-left">
                    <div className="social-title">
                        <h3 className="social-header bottom_orange">Social</h3>
                    </div>
                    <div>
                        {renderTab()}
                    </div>
                </div>
                <SocialTabs />
            </SocialData.Provider>
        </div>

    )
}


export default SocialContainer





















