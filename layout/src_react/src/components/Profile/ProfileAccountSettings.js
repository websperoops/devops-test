import React from 'react'
import "./profile.css";

const ProfileAccountSettings = ({username,email}) => (
    <div className="profile-section profile-account-settings" id="profile-account-settings">
        <div className="profile-section-title">
            <p className="profile-section-header">Account Settings</p>
        </div>
        <div className="profile-section-subtitle">
            <p>User Information</p>
        </div>
        <ul className="profile-section-info-list">
            <li>Username: <span>{username}</span></li>
            <li>Password: <span>*****</span><a className="fa fa-pencil" href="../change_password"></a></li>
            <li>Primary Email: <span>{primary_email}</span><i data-toggle="modal"
                href="#editPrimaryEmail" className="fa fa-pencil"></i></li>
        </ul>

    </div>
)

export default ProfileAccountSettings;