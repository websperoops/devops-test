import React, { Component } from 'react';

class TwitterMention extends Component {
   constructor(props) {
      super(props)
   }

   render() {
      const { item } = this.props

      const formatText = (texts) => {
         texts = texts.replace(' ', ' ')
         let textsArray = texts.split(' ')

         if(textsArray[textsArray.length - 1].includes('https://t.co')) {
            textsArray = textsArray.slice(0, textsArray.length - 1)
         }
         
         const formatUsername = (usernames, idx) => {
            const usernamesArray = usernames.slice(usernames.indexOf('@')+1).split('@')

            return usernamesArray.map(username => {
               return <a href={`https://twitter.com/${username}`} key={username+idx} className='orange-text' target="_blank">{'@' + username + " "}</a>
            })
         }

         const formatHashtag = (hashtags, idx) => {
            const hashtagsArray = hashtags.slice(hashtags.indexOf('#')+1).split('#')

            return hashtagsArray.map(hashtag => {
               return <a href={`https://twitter.com/hashtag/${hashtag}`} key={hashtag+idx} className='orange-text' target="_blank">{'#' + hashtag + " "}</a>
            })
         }

         return textsArray.map((text, idx) => (
            text.includes('@') ? <span key={text+idx}>{formatUsername(text, idx)}</span>
            :
            (
               text.includes('#') ? <span key={text+idx}>{formatHashtag(text, idx)}</span>
               :
               (
                  text.includes('https://t.co') || text.includes('https://twitter.com') ? 
                  <a key={text+idx} href={text} className='orange-text' target="_blank">{text + ' '}</a> : (text + ' ')
               )
            )
         ))
      }

      return (
         <div className="timeline-container-item d-flex flex-column" style={{ minHeight: '75px' }}>
            <img className="timeline-item-icon" src={item.icon} alt="icon" />
            <p className={`timeline-item-text`}>
               You were mentioned in a <a href={`https://twitter.com/i/web/status/${item.mention_id}`} target="_blank" className='orange-text'>Tweet!</a>{" "}
               <span className="timeline-item-text" >{formatText(item.text)}</span>
            </p>

            <p className="timeline-item-date">{item.date}</p>

            <div className="timeline-connector"></div>
         </div>
      )
    }
}

export default TwitterMention;