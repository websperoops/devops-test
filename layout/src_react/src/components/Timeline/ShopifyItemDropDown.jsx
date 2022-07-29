import React, {useState, useEffect, useRef } from 'react';
import './ShopifyItemDropDown.css';

const ShopifyItemDropDown = ({ item, type, children }) => {
  const numberFormat = new Intl.NumberFormat('us-en', { style: 'currency', currency: 'usd' })

  const detailsRef = useRef()
  const [height, setHeight] = useState(null)

  useEffect(()=> {
    setHeight(detailsRef.current.clientHeight)
  },[])

  const renderItems = () => {
    const length = item.line_items.length;

    return (
      item.line_items &&
      item.line_items.map((lineItem, idx) => {
        return (
          <div key={idx}>
            <div className="item-description-details-row">
              <div style={{ width: '70%' }}>{type === 'shopifyOrder' ? lineItem.name : lineItem.title}</div>
              <div style={{ width: '10%', textAlign: 'center' }}>{lineItem.quantity}</div>
              <div style={{width: '20%', textAlign: 'right', paddingRight: '5px'}}>${lineItem.price}</div>
            </div>
            {idx != length - 1 && (
              <div style={{ width: '100%', height: '2px', background: 'lightgrey'}}></div>
            )}
          </div>
        );
      })
    );
  };

  return (
    <div className={`shopify-item-dropdown-container ${children ? "abandoned-dropdown-container" : ""}`}>
      <div className="item-description-container">
        <div className="item-description-header">
          <div className="font-weight-bold" style={{ width: '70%' }}>Item Description</div>
          <div className="font-weight-bold" style={{ width: '10%', textAlign: 'center' }}>Qty</div>
          <div className="font-weight-bold" style={{ width: '20%', textAlign: 'right', paddingRight: height >= 142 ? '15px' : '5px'}}>Price</div>
        </div>
        <div ref={detailsRef} className="item-description-details">{renderItems()}</div>
      </div>

      <div className="summary-container">
        <div className="item-description-header">
          {type === 'shopifyOrder' ? (
            <div className="header-order-summary font-weight-bold">Order Summary</div>
          ) : (
            <div className="header-abandoned-summary font-weight-bold">Abandoned Cart Summary</div>
          )}

          {type === 'shopifyOrder' && (
            <div className="header-order-number font-weight-bold"><a style={{ color: '#ef7c15' }} target="_blank" href={`https://${item.domain}/admin/orders/${item.order_id}`}>#{item.order_number}</a></div>
          )}
        </div>

        <div className="summary-row">
          <span className="summary-row-label">Line Items Total:</span>
          <span className="summary-row-value">{numberFormat.format(item.total_line_items_price)}</span>
        </div>

        <div className="summary-row">
          <span className="summary-row-label">Discount(-):</span>
          <span className="summary-row-value">{numberFormat.format(item.total_discounts)}</span>
        </div>

        <div className="summary-row">
          <span className="summary-row-label">Subtotal:</span>
          <span className="summary-row-value">{numberFormat.format(item.subtotal_price)}</span>
        </div>

        <div className="summary-row">
          <span className="summary-row-label">Shipping:</span>
          <span className="summary-row-value">
            {item.lines
              ? item.lines.length > 0 && numberFormat.format(item.lines[0].discounted_price)
              : numberFormat.format(item.shipping_price)}
          </span>
        </div>

        <div className="summary-row">
          <span className="summary-row-label">Tax:</span>
          <span className="summary-row-value">{numberFormat.format(item.total_tax)}</span>
        </div>

        <div className="summary-row" style={{ borderTop: '2px solid lightgrey' }}>
          <span className="summary-row-label" style={{ paddingTop: '5px' }}>Order Total:</span>
          <span className="summary-row-value">{numberFormat.format(item.total_price)}</span>
        </div>

        {children && (
          <div>{children}</div>
        )}
      </div>
    </div>
  );
};

export default ShopifyItemDropDown;
