import React, { useContext } from 'react'
import FeedAllActivity from './FeedAllActivity'
import FeedConversations from './FeedConversations'
import FeedInteractions from './FeedInteractions'
import FeedFollows from './FeedFollows'
import { SocialData } from './SocialContainer'

const FeedTabSelected = () => {
    const { feedLink } = useContext(SocialData);
    return (
        <div>
            <div style={{ backgroundColor: '#fff', minHeight: '600px', position: 'relative' }} >
                <div className="droptown-option pt-3 ml-3 d-flex flex-row">
                    <select className="ml-3" id="network-feed" defaultValue="Networks">
                        <option disabled>Networks</option>
                    </select>

                    <select className="ml-3" id="network-time" defaultValue="Time">
                        <option disabled>Time</option>
                    </select>
                </div>

                {feedLink === 'All Activity' && <FeedAllActivity /> ||
                    feedLink === 'Conversations' && <FeedConversations /> ||
                    feedLink === 'Interactions' && <FeedInteractions /> ||
                    feedLink === 'Follows' && <FeedFollows />
                }
            </div>
        </div>
    )
}
export default FeedTabSelected
