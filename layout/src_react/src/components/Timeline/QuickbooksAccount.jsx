import React, { Component } from 'react';

class QuickbooksAccount extends Component {
    constructor(props) {
        super(props)
        this.numberFormat = new Intl.NumberFormat('us-en', { style: 'currency', currency: 'usd' })
    }

    render() {
        const { item } = this.props
        return (
            <div className="timeline-container-item d-flex flex-column" style={{ minHeight: '75px' }}>
                <img className="timeline-item-icon" src={item.icon} alt="icon" />
                <p className="timeline-item-text">
                    Your account  <span className="font-weight-bold">{item.name}</span> was updated at
        <span className="font-weight-bold"> {item.data} </span>and now has a balance of <span className="font-weight-bold">{this.numberFormat.format(item.current_balance)}</span>.</p>
                <div className="d-flex flex-row">
                    <p className="timeline-item-date">{item.date}</p>
                </div>
                <div className="timeline-connector"></div>
            </div>
        )
    }
}

export default QuickbooksAccount;