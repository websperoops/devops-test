import React, { Component } from 'react'
import InstagramDropdown from './InstagramDropdown'
import './TimelineItem.css'

class InstagramStory extends Component {
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
                            Your Instagram story has reached {this.formatNumber(item.total_taps_fwd)} {item.total_taps_fwd>1 ? 'people' : 'person'} today!
                        </p>

                        <div className="d-flex flex-row timeline-dropdown-parent">
                            <p className="timeline-item-date" style={{ height: '15px' }}>{item.date}</p>
                            <i onClick={() => this.setState({ showDropList: !showDropList })} className={`fa ${showDropList ? 'fa-angle-up' : 'fa-angle-down'}`}></i>
                        </div>
                    </div>
                </div>

                {
                    showDropList && <InstagramDropdown item={item} type="instagramStory" />
                }
                <div className="timeline-connector"></div>
            </div>
        )
    }
}

export default InstagramStory;
