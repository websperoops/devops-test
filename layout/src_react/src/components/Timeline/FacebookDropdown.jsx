import React, {useEffect, useState} from 'react';
import './FacebookDropdown.css';

const FacebookDropdown = ({ item }) => {
  const [imgLink, setImgLink] = useState('')

  useEffect(() => {
    let tester = new Image();

    tester.src = item.full_picture;
    tester.onload = () => {
      setImgLink(item.full_picture)
    }
    tester.onerror = () => {
      setImgLink('../../../../static/images/no-image.png')
    };
  }, [])

  const formatDate = () => {
    const date = new Date(item.created_time);
    return `${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear()}`;
  };

  const formatNumber = (n) => {
    return new Intl.NumberFormat().format(n)
  }

  const formatMessage = () => {
    let textsArray = item.message.replace(/\n/g,' ').split(' ')

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

  const postPerformance = () => {
    return (
      <div className="facebook-post-performance-container">
        <div className="facebook-post-performance-header">Post Performance</div>

        <div className="facebook-post-details">
          <div className="facebook-post-label-container">
            <div className="facebook-post-label">People Reached</div>
            <div className="facebook-post-label">Likes, Comments & Shares</div>
          </div>
          <div className="facebook-post-value-container">
            <div className="facebook-post-value">{formatNumber(item['impressions']["('Lifetime Post Total Reach',)"])}</div>
            <div className="facebook-post-value">{formatNumber(item['total_reactions'])}</div>
          </div>
        </div>
      </div>
    );
  }

  const reactions = () => {
    return (
      <div className="facebook-post-reactions-container">
        <div className="facebook-post-reactions-header">Reactions</div>

        <div className="facebook-post-reactions-type-container">
          <div className="facebook-post-reactions-type-block" style={{marginLeft: "5px"}}>
            <img className="facebook-post-reactions-type-img" src="../../../../static/images/facebook-like.png"/>
            <div className="facebook-post-reactions-type-value">{item['reactions']["('Lifetime Total Like Reactions of a post.',)"]}</div>
          </div>

          <div className="facebook-post-reactions-type-block">
            <img className="facebook-post-reactions-type-img" src="../../../../static/images/facebook-love.png"/>
            <div className="facebook-post-reactions-type-value">{item['reactions']["('Lifetime Total Love Reactions of a post.',)"]}</div>
          </div>

          <div className="facebook-post-reactions-type-block">
            <img className="facebook-post-reactions-type-img" src="../../../../static/images/facebook-haha.png"/>
            <div className="facebook-post-reactions-type-value">{item['reactions']["('Lifetime Total haha Reactions of a post.',)"]}</div>
          </div>

          <div className="facebook-post-reactions-type-block">
            <img className="facebook-post-reactions-type-img" src="../../../../static/images/facebook-wow.png"/>
            <div className="facebook-post-reactions-type-value">{item['reactions']["('Lifetime Total wow Reactions of a post.',)"]}</div>
          </div>

          <div className="facebook-post-reactions-type-block">
            <img className="facebook-post-reactions-type-img" src="../../../../static/images/facebook-sad.png"/>
            <div className="facebook-post-reactions-type-value">{item['reactions']["('Lifetime Total sad Reactions of a post.',)"]}</div>
          </div>

          <div className="facebook-post-reactions-type-block" style={{marginRight: "5px"}}>
            <img className="facebook-post-reactions-type-img" src="../../../../static/images/facebook-angry.png"/>
            <div className="facebook-post-reactions-type-value">{item['reactions']["('Lifetime Total anger Reactions of a post.',)"]}</div>
          </div>
        </div>
      </div>
    );
  }

  const impressions = () => {
    return (
      <div className="facebook-impressions-reach">
        <div className="facebook-impressions-reach-header">Impressions</div>

        <div className="facebook-post-details">
          <div className="facebook-post-label-container">
            <div className="facebook-post-label">Total Impressions</div>
            <div className="facebook-post-label">Organic Impressions</div>
            <div className="facebook-post-label">Paid Impressions</div>
          </div>
          <div className="facebook-post-value-container">
            <div className="facebook-post-value">{formatNumber(item['total_impressions'])}</div>
            <div className="facebook-post-value">{formatNumber(item['impressions']["('Lifetime Post Organic Impressions',)"])}</div>
            <div className="facebook-post-value">{formatNumber(item['impressions']["('Lifetime Post Paid Impressions',)"])}</div>
          </div>
        </div>
      </div>
    );
  }

  const reach = () => {
    return (
      <div className="facebook-impressions-reach">
        <div className="facebook-impressions-reach-header">Reach</div>
        
        <div className="facebook-post-details">
          <div className="facebook-post-label-container">
            <div className="facebook-post-label">Total Reach</div>
            <div className="facebook-post-label">Organic Reach</div>
            <div className="facebook-post-label">Paid Reach</div>
          </div>
          <div className="facebook-post-value-container">
            <div className="facebook-post-value">{formatNumber(item['impressions']["('Lifetime Post Total Reach',)"])}</div>
            <div className="facebook-post-value">{formatNumber(item['impressions']["('Lifetime Post Organic reach',)"])}</div>
            <div className="facebook-post-value">{formatNumber(item['impressions']["('Lifetime Post Paid Reach',)"])}</div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="facebook-dropdown-container">
      <div className="facebook-dropdown-left">
        {
          imgLink.length > 0 ? (
            <a href={item.permalink} target="_blank"><img className="facebook-img" src={imgLink} /></a>
          ) : <div className="facebook-img"></div>
        }
        <div className="facebook-date"><span style={{color:"gray"}}>Published:</span> {formatDate()}</div>
        <div className="facebook-left-divider"></div>
        <div className="facebook-text">{formatMessage(item.message)}</div>
      </div>
      
      <div className="facebook-dropdown-right">
        {postPerformance()}
        {reactions()}
        <div className="facebook-impressions-reach-container">
          {impressions()}
          {reach()}
        </div>
      </div>
    </div>
  );
};

export default FacebookDropdown;
