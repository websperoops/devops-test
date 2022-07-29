import React from 'react'
const FeedFollowsItem = ({ img, site, followsActiviy, }) => (
    <div className="follows-item">
        <div className="follows-header">
            <img src={img} alt="social-media-site" className="follows-item-icon" />
            <p className="follows-site">{site}</p>
            <p className="follows-item-actions">Actions <i className="fa fa-caret-down"></i></p>
        </div>


        <div className="follows-activity">
            <p className={parseInt(followsActiviy) > 0 ? 'follows-gain' : 'follows-lost'}> {parseInt(followsActiviy) > 0 && '+'} {followsActiviy} Followers</p>
        </div>
    </div>
);

export default FeedFollowsItem;