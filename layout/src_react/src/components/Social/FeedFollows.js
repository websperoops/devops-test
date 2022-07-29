import React from 'react'
import FeedFollowsItem from './FeedFollowsItem'

const FeedFollows = () => (
    <div className="feed-follows">
        <div className="follows-container">
            <FeedFollowsItem img="https://imageog.flaticon.com/icons/png/512/124/124010.png?size=1200x630f&pad=10,10,10,10&ext=png&bg=FFFFFFFF" site="Facebook" followsActiviy="3" />
        </div>
    </div>
)

export default FeedFollows;