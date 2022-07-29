import React from 'react'
import "./profile.css";

const ProfileSidebar = () => (
    <div className="profile-sidebar">
        <div className="mysettings-header">
            <h3>My Settings</h3>
        </div>
        <div className="profile-sidebar-content">
            <ul className="profile-settings-list">
                <li><a className="my-profile-link" href="#my-profile">My Profile</a></li>
                <li> <a className="account-settings-link" href="#profile-account-settings">Account Settings</a></li>
                <li> <a className="notifications-link" href="#profile-notifications-settings">Notifications</a></li>
                <li> <a className="tier-link" href="#subscription-settings">Subscription</a></li>
            </ul>
        </div>
    </div>
);

export default ProfileSidebar;
