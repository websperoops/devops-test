import React from 'react';
import PostEngagement from './PostEngagement';
import './topSocialPost.css';

const PostEngagements = ({ views, likes, shares, comments}) => {
  return (
    <div className='post-engagements-container'>
      <PostEngagement type={'Like'} count={likes}/>
      {
        shares ? <PostEngagement type={'Share'} count={shares}/> : <PostEngagement type={'Comment'} count={comments}/>
      }
      <PostEngagement type={'View'} count={views}/>
    </div>
  );
};

export default PostEngagements;
