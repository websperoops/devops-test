import React, {useState} from 'react';
import Dropdown from './Dropdown'
import './topSocialPost.css';

const TopSocialPostHeader = ({integration, link}) => {
  const [showDropdown, setShowDropdown] = useState(false)
  const options = [ 'View Post' ]

  const toggleDropdown = () => {
    setShowDropdown(preState => !preState)
  }

  return (
    <div className='menu social-post-header'>
      <h5 className='text-capitalize'><img className="integration-img" src={`../../../../static/images/${integration.toLowerCase()}-logo.svg`}/>{integration}</h5>
      <div className='graph-menu-icons'>
        <i onClick={toggleDropdown}
          style={{ cursor: 'pointer' }}
          className='fa fa-caret-down'
        />
      </div>
      {
        showDropdown && link && (
          <>
            <Dropdown toggleDropdown={toggleDropdown} options={options} type={'post'} link={link}/>
          </>
        )
      }
    </div>
  );
};

export default TopSocialPostHeader;