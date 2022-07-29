import React, { Component } from 'react'
import ShopifyItemDropDown from './ShopifyItemDropDown'
import './TimelineItem.css'

class ShopifyOrder extends Component {
    constructor(props) {
        super(props)
        this.state = {
            showDropList: false,
        }
        this.numberFormat = new Intl.NumberFormat('us-en', { style: 'currency', currency: 'usd' })
    }

    render() {
        const { item } = this.props;
        const { showDropList, quantity } = this.state
        return (
            <div className="timeline-item-container" style={{ height: 'auto' }}>
                <div className="timeline-container-item-top">

                    <img className="timeline-item-logo" src={item.icon} alt="icon" />

                    <div className="timeline-item-text-container">
                        <p className="timeline-item-text">
                            <span className="font-weight-bold">{`${item.customer_ref!=null ?item.customer_ref.first_name:'' } ${item.customer_ref!=null ?item.customer_ref.last_name:''}`}</span> 
                            {' placed an order for'} 
                            <span className="font-weight-bold"> {this.numberFormat.format(item.total_price)} </span> with {item.line_items_count} item(s) in it.
                        </p>

                        <div className="d-flex flex-row timeline-dropdown-parent">
                            <p className="timeline-item-date" style={{ height: '15px' }}>{item.date}</p>
                            <i onClick={() => this.setState({ showDropList: !showDropList })} className={`fa ${showDropList ? 'fa-angle-up' : 'fa-angle-down'}`}></i>
                        </div>
                    </div>

                </div>

                {
                    showDropList && <ShopifyItemDropDown item={item} showDropList={showDropList} type="shopifyOrder" />
                }
                <div className="timeline-connector"></div>
            </div>
        )
    }
}

export default ShopifyOrder;
