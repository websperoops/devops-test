import React from 'react'

const FeedActivity = (props) => (
    <div className="feed-activity">
        <div className="activity-header">
            <div className="activity-title">
                <h3 className="activity-title-header">{props.title}</h3>
                <img className="activity-title-icon" src={props.icon} alt="icon" />
            </div>


            <div className="activity-info-container">
                <span className="activity-info">
                    {props.info}
                </span>
            </div>
        </div>


        <span className="activity-time">{props.time}</span>
        <div className="activity-block">
            <img className="activity-img" src={props.img} alt="activity" />
            <div className="activity-description">
                <p>{props.description}</p>
            </div>
        </div>
    </div>
)

export default FeedActivity