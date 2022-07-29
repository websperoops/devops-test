import React from 'react';
import './topSocialPost.css';

const NoTopPost = ({message}) => {
  return <div className='no-top-post'>
     {message}
  </div>;
};

export default NoTopPost;
