import React from 'react';
import { FacebookShareButton, TwitterShareButton } from 'react-share';
import './ReferralsModal.css';
import ReactModal from 'react-modal';

const ReferralsModal = ({ handleClose, affiliate_code, showReferralsModal, username }) => {
  const shareLink = `https://blocklight.io/signup/${affiliate_code}`
  const emailContent = `Good news!%0A%0AYour friend, ${username}, has invited you to join them on the Blocklight Analytics Platform, the all-in-one tool for tracking your business growth.%0A%0ASign up now and you'll receive two months free! Here's how to do it:%0A%0A1. Sign up at blocklight.io/signup/${affiliate_code}%0A%0A2. Start your free 2-month service today!%0A%0AWe look forward to having you join the Blocklight family!`;
  const emailSubject = 'Blocklight Referral Link'

  return (
    <ReactModal
      ariaHideApp={false}
      onRequestClose={handleClose}
      className="referrals-modal-container"
      isOpen={showReferralsModal}
      shouldCloseOnEsc={true}
      shouldCloseOnOverlayClick={true}
    >
      <section className="referrals-header-container">
        <h3 className="referrals-header referrals-header-main">
          Earn 2 <span style={{ color: '#ef7c15' }}>FREE Months</span> of Analytics with Referrals!
        </h3>
        <p className="referrals-header referrals-header-minor">Earn 2 months of PLUS free for each referral for a mazimum of 24 months.</p>
      </section>

      <section className="referrals-images-container">
        <div className="referrals-images-block">
          <img src="../../../../../static/svg/invite_a_friend.svg" />
          <div>
            <p className="referrals-images-number">1</p>
            <p className="referrals-images-text">Invite a Friend</p>
          </div>
        </div>
        <div className="referrals-images-block">
          <img src="../../../../../static/svg/two_months_free.svg" />
          <div>
            <p className="referrals-images-number">2</p>
            <p className="referrals-images-text">Two Months Free</p>
          </div>
        </div>
      </section>

      <section className="referrals-share-container">
        <p className="referrals-share-text">Share with the following methods:</p>
        <div className="referrals-share-buttons-container">
          <a href={`mailto:?subject=${emailSubject}&body=${emailContent}`} className="referrals-share-button">
            <img className="button-logo" src="../../../../../static/svg/envelope-icon.svg"/>Share via Email
          </a>
          <FacebookShareButton url={shareLink} quote='Blocklight Referral Link'>
            <div className="referrals-share-button">
              <img className="button-logo" src="../../../../../static/svg/facebook-icon.svg"/>Share on Facebook
            </div>
          </FacebookShareButton>
          <TwitterShareButton url={shareLink} title='Referral Link'>
            <div className="referrals-share-button">
              <img className="button-logo" src="../../../../../static/svg/twitter-icon.svg"/>Share on Twitter
            </div>
          </TwitterShareButton>
        </div>
      </section>

      <section className="referrals-affiliate-container">
        <p className="referrals-affiliate-text">Have your friends sign up using url:</p>
        <div className="referrals-affiliate-box" onClick={() => navigator.clipboard.writeText(shareLink)}>
          <div className="referrals-affiliate-icon">
            <i className="fa fa-link" />
          </div>
          <div className="referrals-affiliate-link">{`https://blocklight.io/signup/${affiliate_code}`}</div>
        </div>
      </section>

      <button className="referrals-btn referrals-btns-cancel" onClick={handleClose}>Cancel</button>
    </ReactModal>
  );
};

export default ReferralsModal;
