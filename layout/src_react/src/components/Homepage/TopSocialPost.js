import React, { useEffect, useState } from 'react';
import TopSocialPostHeader from './TopSocialPostHeader';
import TopSocialPostContent from './TopSocialPostContent';
import PostEngagements from './PostEngagements';
import NoTopPost from './NoTopPost'
import {
  getFacebookPostsTotalEngagements,
  getFacebookPostsTotalReactions,
  getFacebookPost,
  getFacebookPostImpressions,
  getFacebookPostReactions,
  getInstagramPostsTotalEngagements,
  getInstagramPost,
  getInstagramImpressions } from '../../api/BLApi'

const TopSocialPost = ({ count, integration, time, timeOptions }) => {
  const [postInfo, setPostInfo] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let {since} = timeOptions.find(t => t.name===time)
    
    let postId = null
    let engagement = 0
    let hourFilter = ''

    setLoading(true)

    const getFacebookPostInfo = async () => {
      // find the most engaged Facebook post (sum of engagements count and reactions count)
      const postsEngagements = await getFacebookPostsTotalEngagements(since)
      const postsReactions = await getFacebookPostsTotalReactions(since)

      if(postsEngagements.length){
        for(let i=0; i<postsEngagements.length; i++){
          for(let j=0; j<postsReactions.length; j++){
            if(postsEngagements[i].post_id === postsReactions[j].post_id){
              let total = parseInt(postsEngagements[i].integrations_facebook_page_post_engagements__value__sum) + parseInt(postsReactions[j].integrations_facebook_page_post_reactions__value__sum)
              if(total > engagement) {
                engagement = total
                postId = postsEngagements[i].post_id
              }
              break
            }
          }
        }
  
        const post = await getFacebookPost(postId)
  
        // Get number of post views (The number of times your Page's post entered a person's screen. Posts include statuses, photos, links, videos and more. (Total Count))
        const impressions = await getFacebookPostImpressions(postId)
        const views = parseInt(impressions.find(impression => impression.integrations_facebook_page_post_impressions__name === "('post_impressions',)").integrations_facebook_page_post_impressions__value__sum)
  
        // Get number of likes
        const reactions = await getFacebookPostReactions(postId)
        const likes = parseInt(reactions.find(reaction => reaction.integrations_facebook_page_post_reactions__name.includes('like')).integrations_facebook_page_post_reactions__value__sum)
  
        // set post info
        setPostInfo({
          postId: post.post_id,
          createdDate: post.created_time.slice(0,10),
          message: post.message,
          picture: post.full_picture,
          shares: post.shares ? JSON.parse(post.shares.replace(/'/g,'"')).count : 0,
          views: views,
          likes: likes,
          link: post.permalink
        })
      } else {
        setPostInfo(null)
      }
      setLoading(false)
    }

    const getInstagramPostInfo = async () => {
      // find the most engaged Instagram post
      const postsEngagements = await getInstagramPostsTotalEngagements(since)

      if(postsEngagements.length){
        postsEngagements.forEach(postEngagement => {
          if(parseInt(postEngagement.integrations_instagram_media_insights_engagements__value__sum) > engagement){
            engagement = parseInt(postEngagement.integrations_instagram_media_insights_engagements__value__sum)
            postId = postEngagement.media_id
          }
        })

        const post = await getInstagramPost(postId)

        // Get number of post views (Total number of times the media object has been seen)
        const views = await getInstagramImpressions(postId)

        const comments = parseInt(post.comments_count)
        const likes = engagement - comments

        // set post info
        setPostInfo({
          postId: post.media_id,
          createdDate: post.timestamp.slice(0,10),
          message: post.caption,
          picture: post.media_url,
          comments: comments,
          views: parseInt(views.integrations_instagram_media_insights_impressions__value__sum),
          likes: likes,
          link: post.permalink
        })
      } else {
        setPostInfo(null)
      }
      setLoading(false)
    }

    if(integration === 'Facebook') {
      getFacebookPostInfo()
    }
    else if(integration === 'Instagram') {
      getInstagramPostInfo()
    }
  }, [time]);

  return (
    <div
      className='chart-container homepage-chart-container ml-3'
      style={{ width: '310px' }}
      id={count + '_container'}
    >
      <div className='graph theme-widgets ' style={{overflow:'visible'}}>
        <TopSocialPostHeader integration={integration} link={postInfo ? postInfo.link : null}/>

        {
          loading ? <NoTopPost message='Loading'/> :
          (postInfo ? (
            <>
              <TopSocialPostContent photo={postInfo && postInfo.picture} message={postInfo.message} date={postInfo.createdDate} integration={integration}/>
              <PostEngagements likes={postInfo.likes} views={postInfo.views} shares={postInfo.shares ? postInfo.shares : 0} comments={postInfo.comments ? postInfo.comments : 0}/>
            </>
            )
            :
            <NoTopPost message={`There are no posts in the ${time.toLowerCase()}!`}/>
          )
        }
      </div>
    </div>
  );
};

export default TopSocialPost;