import React, {useEffect, useState} from 'react'
import {Form} from 'react-bootstrap'
import {updateUserProfile, getUserProfile} from '../../api/BLApi'
import "./profile.css";

const ProfileNotificationsSettings = () => {
    const [email, setEmail] = useState();
    const [text, setText] = useState();
    const [userId, setUserId] = useState();

    const onChangeEmail = () => {
        setEmail(!email);
        updateUserProfile({email_notifications_on : !email}, userId)
    }

    const onChangeText = () => {
        setText(!text);
        updateUserProfile({text_notifications_on : !text}, userId)
    }

    useEffect(() => {
        getUserProfile().then(
            data => {
                setUserId(data.results[0].id); // find user id
                setEmail(data.results[0].email_notifications_on);
                setText(data.results[0].text_notifications_on);
            }
        )
    }, [])


    return (

    
    <div className="profile-section profile-notifications" id="profile-notifications-settings">
        <div className="profile-section-title">
            <p className="profile-section-header">Notifications</p>
        </div>
        <div className="profile-section-subtitle">
            <p>General</p>
        </div>
        
        <Form>
        <ul className="profile-section-info-list">
            <li>
                <Form.Check 
                    type="checkbox" 
                    id="email-notifications" 
                    label="Recieve email notifications" 
                    htmlFor="email-notifications"
                    defaultChecked={email}
                    onClick={onChangeEmail} />
            </li>
            <li>
                <Form.Check 
                    type="checkbox" 
                    id="text-notifications" 
                    label="Recieve text notifications:" 
                    htmlFor="text-notifications" 
                    defaultChecked={text} 
                    onClick={onChangeText} />
            </li>
        </ul>
        </Form>
    </div>
    )
}

export default ProfileNotificationsSettings;