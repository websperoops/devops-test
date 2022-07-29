import React, { Component } from 'react';
import ReactModal from 'react-modal'
import { sendAbandonedCartEmail } from '../../api/BLApi'

class AbandonedCartModal extends Component {
    constructor(props) {
        super(props)

        this.state = {
            sendEmail: false
        }
        this.numberFormat = new Intl.NumberFormat('us-en', { style: 'currency', currency: 'usd' })
        this.handleSendingEmail = this.handleSendingEmail.bind(this)
    }

    componentDidMount() {
        let item = this.props.item;
        item.line_items.map((item, i) => {
            let img = item.product_ref && item.product_ref.images.length > 0 ? item.product_ref.images[0].src : 'https://dev.blocklight.io/static/images/not-found.png';
            img = item.variant_ref && item.variant_ref.image ? item.variant_ref.image.src : img
            item.image = img;
            item.product = item.variant_ref && item.variant_ref.title !== 'Default Title' ? `${item.title} - ${item.variant_ref.title}` : item.title
        })

        this.setState({ item })
    }

    handleSendingEmail() {
        sendAbandonedCartEmail(this.state.item)
            .then(data => {
                if (data.success) {
                    this.setState({ sendEmail: true })
                }
            })
        setTimeout(this.props.close, 3000)
    }

    render() {
        const { props, numberFormat } = this
        return (
            <ReactModal ariaHideApp={false} onRequestClose={props.close} isOpen={props.isOpen} shouldCloseOnEsc={true} shouldCloseOnOverlayClick={true} className="modal-outer abandoned-cart-email-outer" >
                <div className="abandoned-cart-email ">
                    {this.state.sendEmail && <div className="aler alert-success">
                        <p className="p-3">Email Send Succesfully!</p>
                    </div>}
                    <div className="d-flex flex-column justify-content-center">
                        <p style={{ borderBottom: 'none', fontFamily: 'open sans', fontSize: '2.5rem', fontWeight: 'bolder' }} className="text-center">Forget Something?</p>
                        <img className="mx-auto" src="/static/images/icon-abandonedcart.svg" alt="abadoned-cart-icon" width={120} height={80} />
                        <p className="mt-3" style={{ fontSize: '14px', color: '#8d8d8d' }}>We noticed you left some things behind.</p>
                        <div className="d-flex flex-column abandoned-items-container mx-auto">
                            <div className="abandoned-items-header d-flex flex-row align-items-center" style={{ background: '#d1d1d1', height: '25px' }}>
                                <p className="mt-3" style={{ marginRight: '56%', marginLeft: '20px' }}>Item</p>
                                <p className="mr-5 mt-3">Qty</p>
                                <p className="ml-md-3 mt-3">Total</p>
                            </div>
                            {props.item.line_items.map((item, i) => {
                                return <div style={item.title.length > 20 ? { height: 'auto' } : { height: '100px' }} key={i} className="d-flex flex-row mx-auto abandoned-cart-item font-weight-bold align-items-center">
                                    <div className="d-flex flex-row align-items-center">
                                        <img width={50} src={item.image} alt='item' />
                                        <p className="mt-3 ml-2 text-left">{item.product}</p>
                                    </div>
                                    <p className="mr-4 mt-2">{item.quantity}</p>
                                    <p className="mt-2">${item.price}</p>
                                </div>
                            }
                            )}

                            <div className="abandoned-cart-price mt-4 font-weight-bold text-right d-flex flex-row justify-content-end">
                                <div className="d-flex flex-column abandoned-cart-price-item">
                                    <p>Discounts(-):</p>
                                    <p>Subtotal:</p>
                                    <p>Shipping:</p>
                                    <p>Tax:</p>
                                    <p className="mt-2 mb-2">Total:</p>
                                </div>
                                <div className="d-flex flex-column abandoned-cart-price-item">
                                    <span>{numberFormat.format(props.item.total_discounts)}</span>
                                    <span>{numberFormat.format(props.item.subtotal_price)}</span>
                                    <span>{numberFormat.format(props.item.shipping_price)}</span>
                                    <span>{numberFormat.format(props.item.total_tax)}</span>
                                    <span className="mt-1 mb-2">{numberFormat.format(props.item.total_price)}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <p className="text-center font-weight-bold mt-3" style={{ color: '#8d8d8d', fontSize: '16px' }}>Let's complete your order!</p>
                    <a href={props.item.abandoned_checkout_url} target="_blank" className="btn_orange mx-auto btn_long" style={{ height: '30px', padding: '6px', display: 'inline-block' }}>Resume Checkout</a>

                    <div className="d-flex flex-row justify-content-center align-items-center border-top btn-container">
                        <button onClick={this.props.close} style={{ height: '30px' }} className="btn_clear btn_long">Don’t Send!</button>
                        <button onClick={this.handleSendingEmail} style={{ height: '30px' }} className="btn_orange btn_long ml-3">Looks Good, Send It!</button>
                    </div>

                </div>
            </ReactModal >
        )
    }
}

export default AbandonedCartModal
