import React from 'react'
import "./profile.css";

class SubscriptionSettings extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      creditCardInfo: null,
      currentTier: null,
      requestedTierChange: null,
      nextPaymentPrice: null,
      nextPaymentDate: null,
    }
  }

  componentDidMount() {
    $.get('/tiers/subscription_info/').done((result) => {
      this.setState({
        creditCardInfo: (result.card_last4 != null) ? {cardLastNumbers: result.card_last4}: null,
        currentTier: {
          name: result.current_tier.name,
          recurringPeriod: result.current_tier.recurring_period,
          publicName: result.current_tier.public_name,
        },
        requestedTierChange: (result.requested_tier_change != null) ? {
          name: result.requested_tier_change.name,
          recurringPeriod: result.requested_tier_change.recurring_period,
          publicName: result.requested_tier_change.public_name,
        } : null,
        requestedCancel: result.requested_cancel,
        nextPaymentPrice: result.next_payment_price,
        nextPaymentDate: (result.next_payment_date != null ) ?
          new Date(result.next_payment_date):
          null,
        nextPaymentDateFmt: (result.next_payment_date != null ) ?
        Intl.DateTimeFormat().format(new Date(result.next_payment_date)):
        null,
      });
    }).fail( (error) => {
      console.log("Error loading subscription info:");
      console.log(error);
    });

  }

  render() {
    return (
        <div className="profile-section profile-payment" id="subscription-settings">
          <div className="profile-section-title">
              <p className="profile-section-header">Subscription</p>
          </div>
          {(this.state.requestedCancel == false) && (this.state.requestedTierChange) && (
            [
              <div className="profile-section-subtitle">
                  <p>Next Payment Day</p>
              </div>,
              <ul className="profile-section-info-list">
                  <li>
                    Your next payment is <b><u>${Math.round(this.state.nextPaymentPrice/100, 2).toFixed(2)}</u></b>
                    &nbsp;for <b><u>{(this.state.requestedTierChange == null ) ?
                          this.state.currentTier.publicName :
                          this.state.requestedTierChange.publicName
                        }</u></b>
                    &nbsp;on <b><u>{this.state.nextPaymentDateFmt}</u></b>.
                  </li>
              </ul>
            ]
          )}
          <div className="profile-section-subtitle">
              <p>Billing Information</p>
          </div>
          <ul className="profile-section-info-list">
              <li>Credit Card: {
                  (this.state.creditCardInfo != null) && (
                    [
                      <span>*{this.state.creditCardInfo.cardLastNumbers}</span>,
                      <a href="/stripe/change_credit_card/"><i className="fa fa-pencil"></i></a>,
                    ]
                )}
              </li>

              <li>Current Subscription: {
                  (this.state.currentTier != null) && (
                    <span>{this.state.currentTier.publicName}</span>
                  )
                }
                <div className="buttons">
                {(this.state.currentTier != null) && (this.state.requestedTierChange != null) && (
                    <span className="gray-text"><i>Ending {this.state.nextPaymentDateFmt}</i></span>
                ) || (
                    (this.state.currentTier != null) && (this.state.requestedCancel == false) && (
                      [
                        <button data-toggle="modal" href="#changeTier" type="submit" className="subscription-btn_orange">Change</button>,
                        <form>
                          <button data-toggle="modal" href="#cancelTier" type="submit" className="subscription-btn_gray">Cancel</button>
                        </form>,
                      ]
                    ) || (this.state.currentTier != null) && (
                      [
                        <span className="gray-text"><i>Ends {this.state.nextPaymentDateFmt}</i></span>,
                        <form action="/tiers/cancel_requested_cancel_tier/" method="GET">
                          <button type="submit" className="subscription-btn_orange">Restart</button>
                        </form>
                      ]
                    )
                  )
                }
                </div>
              </li>
              {(this.state.requestedTierChange != null) && (
              <li>Pending Subscription:
                      <span> {this.state.requestedTierChange.publicName}</span>
                      <div className="buttons">
                      <span className="gray-text"><i>Starts {this.state.nextPaymentDateFmt}</i></span>
                        <form>
                          <button data-toggle="modal" href="#cancelPendingTier" className="subscription-btn_gray">
                            Cancel
                          </button>
                        </form>
                      </div>
              </li>
              )}
          </ul>
    </div>)
  }
}

export default SubscriptionSettings;
