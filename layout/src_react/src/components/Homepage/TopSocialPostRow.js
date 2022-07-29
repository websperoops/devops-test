import React, { useState, useEffect } from 'react';
import { getSocialTimeRange } from '../../api/BLApi'
import TopSocialPost from './TopSocialPost';
import HomepageHeaderDropdown from './HomepageHeaderDropdown';

const TopSocialPostRow = () => {
  const [time, setTime] = useState('Past 3 Months')
  const [timeOptions, setTimeOptions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getSocialTimeRange().then(response => {
      setTimeOptions(response)
      setLoading(false)
    }).catch(err => {
      console.log(err)
    })
  }, [])

  return (
    <div className='d-flex flex-wrap' id="top-post-container-id">
      {
        !loading && 
        <>
          <TopSocialPost count={1} integration={'Facebook'} time={time} timeOptions={timeOptions}/>
          <TopSocialPost count={2} integration={'Instagram'} time={time} timeOptions={timeOptions}/>
          <HomepageHeaderDropdown
            time={time}
            selectTime={(t) => setTime(t)}
            options={timeOptions.filter(option => option.name !== 'Past Hour').map(option => option.name)}
            type={'top-social-post'}
          />
        </>
      }
    </div>
  );
};

export default TopSocialPostRow;
