import React, { Component } from 'react';
import QuickbooksItemDropDown from './QuickbooksItemDropDown'

class QuickbooksBill extends Component {
    constructor(props) {
        super(props)
        this.numberFormat = new Intl.NumberFormat('us-en', { style: 'currency', currency: 'usd' })

        this.state = {
            showDropList: false,
            dueDate: new Date(props.item.due_date).toLocaleString('en-US', { hour12: true, month: 'short', year: 'numeric', day: '2-digit' })
        }
    }

    render() {
        const { item } = this.props
        const { showDropList, dueDate } = this.state
        return (
            <div className="timeline-container-item d-flex flex-column" style={{ height: showDropList ? '250px' : '75px' }}>
                <img className="timeline-item-icon" src={item.icon} alt="icon" />
                <p className="timeline-item-text">
                    Your upcoming bill  <span className="font-weight-bold">{item.account_name}</span> to
        <span className="font-weight-bold"> {item.vendor_name} </span>is due on <span className="font-weight-bold">{dueDate}</span>.</p>
                <div className="d-flex flex-row timeline-dropdown-parent">
                    <p className="timeline-item-date">{item.date}</p>
                    <i onClick={() => this.setState({ showDropList: !showDropList })} className={`fa ${showDropList ? 'fa-angle-up' : 'fa-angle-down'}`}></i>
                    <QuickbooksItemDropDown item={item} showDropList={showDropList} />
                </div>
                <div className="timeline-connector"></div>
            </div>
        )
    }
}

export default QuickbooksBill;