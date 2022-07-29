import React, { useContext, useState, useEffect } from 'react'
import FeedActivity from './FeedActivity'
import { SocialData } from './SocialContainer'
import { csrf_token } from '../../functions/dashboard/dashFunctions'
const FeedAllActivity = () => {
    const context = useContext(SocialData)
    const mentions = context.twitterMentions

    return (
        <div className="all-activity" >
            {
                mentions && mentions.map((mention, i) => {
                    let date = new Date(mention.fields.timestamp)
                    date = date.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true, month: 'short', year: 'numeric', day: '2-digit' })
                    mention.date = date
                    return <div key={i} className="mention rounded p-4 m-3">
                        <p style={{ marginTop: '-10px', marginLeft: '10px' }}> <i className="fa fa-twitter"></i><span className="font-weight-bold ml-4">{mention.fields.other_user_name}</span>  mentioned you</p>
                        <p className="small" style={{ marginTop: '-10px', marginLeft: '35px' }}>{mention.date}</p>
                        <p className="mention_text">{mention.fields.text}</p>
                        <div class="dropdown">
                            <a
                                class="btn btn-secondary dropdown-toggle text-dark"
                                href="#"
                                role="button"
                                id="dropdownMenuLink"
                                data-toggle="dropdown"
                                aria-haspopup="true"
                                aria-expanded="false">
                                Actions
  </a>

                            <div class="dropdown-menu bg-light" aria-labelledby="dropdownMenuLink">
                                <a target="_blank" class="dropdown-item text-dark" href={`https://twitter.com/${mention.fields.other_user_name}/status/${mention.fields.mention_id}`}>View on Platform</a>
                            </div>
                        </div>
                        {/* 
                        <form method="POST" action='/dashboards/social/reply_to_tweet/'>
                            <input type="hidden" name="csrfmiddlewaretoken" value={csrf_token} />
                            <input type="hidden" name="mention_id" value={mention.fields.mention_id} />
                            <input type="hidden" name="screen_name" value={mention.fields.other_user_name} />

                            <input type="text" name="text" className="form-control bg-light text-dark border-light" style={{ width: '100%', borderRadius: '25px', fontSize: '12px' }} placeholder="post a comment" />
                        </form> */}

                        <div className="activity-connector"></div>

                    </div>

                })
            }

        </div>
    )
}

export default FeedAllActivity;