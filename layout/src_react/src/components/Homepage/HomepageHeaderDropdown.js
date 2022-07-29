import React, { useState } from 'react';
import Dropdown from './Dropdown';
import './summaryMetrics.css'; 

const HomepageHeaderDropdown = ({ time, selectTime, options, type}) => {
  const [showDropdown, setShowDropdown] = useState(false);

  const toggleDropdown = () => {
    setShowDropdown((preState) => !preState);
  };

  const clickTime = (t) => {
    selectTime(t)
    setShowDropdown(false)
  }

  return (
    <span className={`homepage-header-dropdown homepage-${type}`} id="top-post-container-id summary-container-id">
      <span className='homepage-header-dropdown-block' onClick={toggleDropdown}>{time}</span>
      {showDropdown && <Dropdown toggleDropdown={toggleDropdown} options={options} type={'time'} clickTime={clickTime}/>}
    </span>
  );
};

export default HomepageHeaderDropdown;
