import React, {useEffect, useState} from 'react';
import './InstagramDropdown.css';

const InstagramDropdown = ({item, type}) => {
  const [imgLink, setImgLink] = useState('')

  useEffect(() => {
    let tester = new Image();

    tester.src = item.media_url;
    tester.onload = () => {
      setImgLink(item.media_url)
    }
    tester.onerror = () => {
      setImgLink('../../../../static/images/no-image.png')
    };
  }, [])

  const formatDate = () => {
    const date = new Date(item.timestamp)
    return `${date.getMonth()+1}/${date.getDate()}/${date.getFullYear()}`
  }

  const formatNumber = (n) => {
    return new Intl.NumberFormat().format(n)
  }

  const formatMessage = () => {
    let textsArray = item.caption.replace(/\n/g,' ').split(' ')

    return textsArray.map((text, idx) => (
      text.includes('#') ? <a key={text+idx} className='orange-text' href={`https://www.instagram.com/explore/tags/${text.slice(1)}`} target="_blank">{text + " "}</a> : (
        text.includes('@') ? <a key={text+idx} className='orange-text' href={`https://www.instagram.com/${text.slice(1)}`} target="_blank">{text + " "}</a> : (text + ' ')
        )
      )
    )
  }

  const postPerformance = () => {
    return(
      <div className="instagram-performance-container">
        <div className="instagram-performance-label-container">
          <div className="instagram-performance-label">Total Engagements</div>
          <div className="instagram-performance-label">Total Impressions</div>
          <div className="instagram-performance-label">Total Reach</div>
          <div className="instagram-performance-label">Total Saved</div>
          <div className="instagram-performance-label">Total Vide Views</div>
        </div>
        <div className="instagram-performance-value-container">
          <div className="instagram-performance-value">{formatNumber(item.total_engagement)}</div>
          <div className="instagram-performance-value">{formatNumber(item.total_impressions)}</div>
          <div className="instagram-performance-value">{formatNumber(item.total_reach)}</div>
          <div className="instagram-performance-value">{formatNumber(item.total_saved)}</div>
          <div className="instagram-performance-value">{formatNumber(item.total_video_views)}</div>
        </div>
      </div>
    )
  }

  const storyPerformance = () => {
    return (
      <div className="instagram-performance-container">
        <div className="instagram-performance-label-container">
          <div className="instagram-performance-label">Total Exits</div>
          <div className="instagram-performance-label">Total Replies</div>
          <div className="instagram-performance-label">Total Tap(Forward)</div>
          <div className="instagram-performance-label">Total Tap(Backward)</div>
        </div>
        <div className="instagram-performance-value-container">
          <div className="instagram-performance-value">{formatNumber(item.total_exits)}</div>
          <div className="instagram-performance-value">{formatNumber(item.total_replies)}</div>
          <div className="instagram-performance-value">{formatNumber(item.total_taps_fwd)}</div>
          <div className="instagram-performance-value">{formatNumber(item.total_taps_back)}</div>
        </div>
      </div>
    )
  }

  return (
    <div className="instagram-dropdown-container">
      <div className="instagram-dropdown-left">
        {
          imgLink.length > 0 ? (
            <a href={item.permalink} target="_blank"><img className="instagram-img" src={imgLink} /></a>
          ) : <div className="instagram-img"></div>
        }
        <div className="instagram-date"><span style={{color:"gray"}}>Published:</span> {formatDate()}</div>
        <div className="instagram-left-divider"></div>
        <div className="instagram-text">{formatMessage()}</div>
      </div>
      
      <div className="instagram-dropdown-right">
        <div className="instagram-performance-header">Post Performance</div>
        <div className="instagram-right-divider"></div>
        {
          type === 'instagramPost' ? postPerformance() : storyPerformance()
        }
      </div>
    </div>
  );
};

export default InstagramDropdown;
