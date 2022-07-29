import React from 'react'
import "./profile.css";

const ProfileSecuritySettings = () => (
    <div className="profile-section profile-security-settings" id="profile-security-settings">
        <div className="profile-section-title">
            <p className="profile-section-header">Privacy & Security</p>
        </div>
        <div className="profile-section-subtitle">
            <p>Discoverability</p>
        </div>
        <ul className="profile-section-info-list">
            <li><label htmlFor="profile-visible">Your profile can be seen:</label> <input type="checkbox"
                id="profile-visible" />
            </li>
            <li><label htmlFor="email-visible">Your email address can be seen:</label> <input
                type="checkbox" id="email-visible" />
            </li>
            <li><label htmlFor="number-visible">Your phone number can be seen:</label> <input
                type="checkbox" id="number-visible" />
            </li>

            <li><label htmlFor="send-receive-messages">Send/receive messages:</label> <input type="checkbox"
                id="send-receive-messages" />
            </li>
        </ul>

    </div>
)

export default ProfileSecuritySettings;