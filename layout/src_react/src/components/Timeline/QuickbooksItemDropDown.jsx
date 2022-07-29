import React from 'react'

const QuickbooksItemDropDown = ({ item, showDropList }) => {

    const numberFormat = new Intl.NumberFormat('us-en', { style: 'currency', currency: 'usd' })

    return (
        <div style={{ minHeight: '150px' }} className={`d-flex flex-column flex-wrap ${showDropList ? 'timeline-item-droplist ' : 'timeline-item-droplist-hidden'}`} >
            <div className='d-flex flex-column flex-wrap'>
                <div className="d-flex flex-row" style={{ borderBottom: '1px solid #d7d7d7', borderTop: '1px solid #d7d7d7' }}>
                    <p style={{ width: '100px' }} className="mr-3 font-weight-bold">Item</p>
                    <p style={{ width: '100px' }} className="mr-3 font-weight-bold">Description</p>
                    <p style={{ width: '45px' }} className="mr-3 font-weight-bold text-right">Price</p>
                    <p className="ml-3 mr-3 font-weight-bold" style={{ width: '14px' }}>Qty</p>
                    <p className="text-right font-weight-bold" style={{ width: '50px' }}>Total</p>
                </div>
                {item.line_items && item.line_items.map((item, i) => {
                    return (
                        <div key={i} className="timeline-droplist-item d-flex flex-row mt-1 align-items-center">
                            <p style={{ width: '100px' }} className="mr-3">{item.item_name}</p>
                            <p style={{ width: '100px', wordBreak: 'break-word' }} className="mr-3">{item.description}</p>
                            <p className="text-right" style={{ minWidth: '50px', marginRight: '15px' }}>{numberFormat.format(Number(item.unit_price))}</p>
                            <p className="mr-3 ml-3" style={{ width: '14px' }}>{item.quantity}</p>
                            <p className="text-right" style={{ width: '50px' }}>{numberFormat.format(Number(item.amount))}</p>
                        </div>
                    )
                })}
            </div>

            {/* <div className="d-flex flex-column timeline-order-summary">
                <div style={{ borderBottom: '1px solid #d7d7d7', borderTop: '1px solid #d7d7d7' }}>
                    {type == 'shopifyOrder' ? <p className="font-weight-bold">Order Summary <span className="font-weight-bold"><a style={{ color: '#ef7c15' }} target="_blank" href={`https://${item.domain}/admin/orders/${item.order_id}`}>#{item.order_number}</a></span></p> : <p className="abandoned-cart-p font-weight-bold">Abandoned Cart Summary</p>}
                </div>
                <div><p>Line Items Total:</p><span className="ml-3">{numberFormat.format(item.total_line_items_price)}</span></div>
                <div><p>Discounts(-):</p> <span className="ml-3">{numberFormat.format(item.total_discounts)}</span></div>
                <div><p>Subtotal:</p> <span className="ml-3">{item.subtotal_price ? numberFormat.format(item.subtotal_price) : '0.00'}</span></div>
                <div><p>Shipping:</p> <span>{item.lines ? item.lines.length > 0 && numberFormat.format(item.lines[0].discounted_price) : item.shipping_price}</span></div>
                <div className="mb-2"><p>Tax: <span className="ml-3">{numberFormat.format(item.total_tax)}</span></p></div>
                <div className="pt-2" style={{ borderTop: '1px solid #d7d7d7' }}><p>Order Total:  <span className="ml-3">{numberFormat.format(item.total_price)}</span></p></div>
            </div> */}
        </div>

    )
}

export default QuickbooksItemDropDown;
