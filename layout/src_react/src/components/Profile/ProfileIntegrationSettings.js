import React from 'react'
import "./profile.css";

const ProfileIntegrationSettings = () => (

    <div className="profile-section" id="profile-integrations-settings">
        <div className="profile-section-title">
            <p className="profile-section-header">Integrations</p>
        </div>
        <div className="profile-section-subtitle">
            <p>Synchronization</p>
        </div>
        <ul className="profile-section-info-list">
            <li><label htmlFor="auto-sync">Automatically sync integrations:</label>
                <select>
                    <option value="Frequency" defaultValue>Frequency</option>
                </select>
                <input type="checkbox" id="auto-sync" />
            </li>
        </ul>
    </div>
)

export default ProfileIntegrationSettings;