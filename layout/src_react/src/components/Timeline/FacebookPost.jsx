import React, { Component } from 'react'
import FacebookDropdown from './FacebookDropdown'
import './TimelineItem.css'

class FacebookPost extends Component {
    constructor(props) {
        super(props)
        this.state = {
            showDropList: false,
        }
    }

    formatNumber(n) {
        return new Intl.NumberFormat().format(n)
    }

    render() {
        const { item } = this.props;
        const { showDropList } = this.state
        return (
            <div className="timeline-item-container" style={{ height: 'auto' }}>
                <div className="timeline-container-item-top">

                    <img className="timeline-item-logo" src={item.icon} alt="icon" />

                    <div className="timeline-item-text-container">
                        <p className="timeline-item-text">
                            {this.formatNumber(item.total_impressions)} {item.total_impressions>1 ? 'people' : 'person'} have seen your post!
                        </p>

                        <div className="d-flex flex-row timeline-dropdown-parent">
                            <p className="timeline-item-date" style={{ height: '15px' }}>{item.date}</p>
                            <i onClick={() => this.setState({ showDropList: !showDropList })} className={`fa ${showDropList ? 'fa-angle-up' : 'fa-angle-down'}`}></i>
                        </div>
                    </div>
                </div>

                {
                    showDropList && <FacebookDropdown item={item} />
                }
                <div className="timeline-connector"></div>
            </div>
        )
    }
}

export default FacebookPost;
