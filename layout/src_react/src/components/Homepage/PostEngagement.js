import React from 'react';
import './topSocialPost.css';

const PostEngagement = ({type, count}) => {
  const formatNumber = (n) => {
    return new Intl.NumberFormat().format(n)
  }

  return (
    <div className={`post-engagement ${type !== 'View' && 'post-engagement-right-border'}`}>
      <div>{formatNumber(count)}</div>
      <div style={{ color: 'grey' }}>{type}{count>1 || count===0 ? 's' : ''}</div>
    </div>
  );
};

export default PostEngagement;
