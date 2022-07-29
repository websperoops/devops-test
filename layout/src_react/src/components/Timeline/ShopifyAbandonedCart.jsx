import React, { Component } from 'react';
import AbandonedCartModal from './AbandonedCartModal';
import ShopifyItemDropDown from './ShopifyItemDropDown'
import './TimelineItem.css'

class ShopifyAbandonedCart extends Component {
    constructor(props) {
        super(props);

        this.state = {
            showDropList: false,
            showAbandonedCartModal: false
        }
        this.numberFormat = new Intl.NumberFormat('us-en', { style: 'currency', currency: 'usd' })
    }

    render() {
        const { item } = this.props;
        const { showDropList, showAbandonedCartModal } = this.state
        const name = item.customer_ref ? `${item.customer_ref.first_name} ${item.customer_ref.last_name}` : ''
        return (
            <>
                <AbandonedCartModal item={item} isOpen={showAbandonedCartModal} close={() => this.setState({ showAbandonedCartModal: false })} />
                <div className="timeline-item-container" style={{ position: 'relative', height: showDropList ? 'auto' : '75px' }} >
                    <div className="timeline-container-item-top">

                        <img className="timeline-item-logo" src={item.icon} alt="icon" />

                        <div className="timeline-item-text-container">
                            <p className="timeline-item-text">
                                <span className="font-weight-bold">{name}</span> just abandoned a cart worth
                                <span className="font-weight-bold"> {this.numberFormat.format(item.total_price)} </span>with {item.line_items_count} item(s) in it.
                            </p>

                            <div className="d-flex flex-row timeline-dropdown-parent">
                                <p className="timeline-item-date" style={{ height: '15px' }}>{item.date}</p>
                                <i onClick={() => this.setState({ showDropList: !showDropList })} className={`fa ${showDropList ? 'fa-angle-up' : 'fa-angle-down'}`}></i>
                            </div>
                        </div>

                    </div>

                    <div className="timeline-connector"></div>
                    {
                        showDropList && 
                            <ShopifyItemDropDown item={item} showDropList={showDropList} type="abandonedCart">
                                <button onClick={() => this.setState({ showAbandonedCartModal: true })} className="btn_orange timeline-item-btn">Recover</button>
                            </ShopifyItemDropDown>
                    }
                </div>
            </>
        )
    }
}

export default ShopifyAbandonedCart;