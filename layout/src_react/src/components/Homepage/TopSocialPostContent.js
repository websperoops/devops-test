import React, { useState, useEffect } from 'react';
import './topSocialPost.css';

const TopSocialPostContent = ({photo, message, date, integration}) => {
  const [imgLink, setImgLink] = useState('')

  useEffect(() => {
    let tester = new Image();

    tester.src = photo;
    tester.onload = () => {
      setImgLink(photo)
    }
    tester.onerror = () => {
      setImgLink('../../../../static/images/no-image.png')
    };
  }, [])

  const formatIgMessage = () => {
    let textsArray = message.replace(/\n/g,' ').split(' ')

    return textsArray.map((text, idx) => (
      text.includes('#') ? <a key={text+idx} className='orange-text' href={`https://www.instagram.com/explore/tags/${text.slice(1)}`} target="_blank">{text + " "}</a> : (
        text.includes('@') ? <a key={text+idx} className='orange-text' href={`https://www.instagram.com/${text.slice(1)}`} target="_blank">{text + " "}</a> : (text + ' ')
        )
      )
    )
  }

  const formatFbMessage = () => {
    let textsArray = message.replace(/\n/g,' ').split(' ')

    return textsArray.map((text, idx) => (
      text.includes('#') ? (
        <a key={text+idx} className='orange-text' href={`https://www.facebook.com/hashtag/${text.slice(1)}`} target="_blank">
          {text + " "}
        </a>
        ) : text.includes('@') ? (
        <a key={text+idx} className='orange-text' href={`https://www.facebook.com/${text.slice(1)}`} target="_blank">
          {text + " "}
        </a>
        ) : text.includes('http') ? (
          <a key={text+idx} className='orange-text' href={text} target="_blank">
            {text + " "}
          </a>
        ) : (text + ' ')
      )
    )
  }

  const formatDate = () => {
    const year = date.slice(0,4)
    const month = parseInt(date.slice(5,7))-1
    const day = date.slice(8)
    const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December',]

    return `${months[month]} ${day}, ${year}`
  }

  return (
    <div className="post-content">
      <div>
        {
          imgLink.length > 0 &&
          <div className="post-img-container">
              <img src={imgLink} className="post-img" />
          </div>
        }

        <h5 className='text-capitalize posted-date'>
          Posted:
          <span className="date-format">{formatDate()}</span>
        </h5>

        <div className='top-social-post-message'>
          {integration === 'Facebook' ? formatFbMessage() : formatIgMessage()}
        </div>
      </div>
    </div>
  );
};

export default TopSocialPostContent;
