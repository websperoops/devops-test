import React from 'react'
import "./profile.css";

const ProfilePaymentSettings = () => (
    <div className="profile-section profile-payment" id="profile-payment-settings">
        <div className="profile-section-title">
            <p className="profile-section-header">Payments</p>
        </div>
        <div className="profile-section-subtitle">
            <p>Billing Information</p>
        </div>
        <ul className="profile-section-info-list">
            <li><label htmlFor="billing">Make secure payments using my:</label>
                <select>
                    <option value="" defaultValue>Method</option>
                </select>
            </li>
        </ul>
        <form className="billing-form">
            <div className="billing-form-input-container">
                <label>First Name:</label>
                <input type="text" id="first-name" />
            </div>

            <div className="billing-form-input-container">
                <label>Last Name:</label>
                <input type="text" id="last-name" />
            </div>

            <div className="billing-form-input-container">
                <label htmlFor="credit-card-number">Credit Card Number:</label>
                <input type="number" id="credit-card-number" />
            </div>

            <div className="billing-form-input-container">
                <label htmlFor="exp-date">Expiration Date:</label>
                <input type="number" id="exp-date" />
            </div>
            <div className="billing-form-input-container">
                <label htmlFor="cvc">CVC:</label>
                <input type="number" id="cvc" /> <i className="fa fa-question-circle question-cvc"></i>
            </div>
        </form>

    </div>
)

export default ProfilePaymentSettings;