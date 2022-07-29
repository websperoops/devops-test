import React, { Component } from 'react';

class EtsyOrder extends Component {
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
                    <span className="font-weight-bold">{item.name}</span> just placed an order
for <span className="font-weight-bold"> {this.numberFormat.format(item.buyer_adjusted_grandtotal)} </span></p>
                <div className="d-flex flex-row">
                    <p className="timeline-item-date">{item.date}</p>
                </div>
                <div className="timeline-connector"></div>
            </div>
        )
    }
}

export default EtsyOrder;