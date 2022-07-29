import React from 'react'
import ProfileSidebar from './ProfileSidebar';
import MyProfile from './MyProfile';
import ProfileAccountSettings from './ProfileAccountSettings';
import ProfileNotificationsSettings from './ProfileNotificationSettings';
import ProfileMobileHeader from './ProfileMobileHeader';
import SubscriptionSettings from './SubscriptionSettings';
import "./profile.css";




const Profile = () => {
    return (
        <div className="profile-container">
            <ProfileSidebar />
            <div className="profile-divider">
                <ProfileMobileHeader />
                <MyProfile />
                {/* <ProfileAccountSettings /> */}
                {/* <ProfileSecuritySettings /> */}
                <ProfileNotificationsSettings />
                <SubscriptionSettings />
                {/* <ProfileIntegrationSettings /> */}

            </div>
        </div>
    )
}

export default Profile
