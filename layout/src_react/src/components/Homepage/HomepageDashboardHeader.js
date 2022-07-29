import React from 'react'
import HomepageHeaderDropdown from './HomepageHeaderDropdown';
import './summaryMetrics.css';

function HomepageDashboardHeader(props) {
    return (
        <div className="homepage-item-title theme-text theme-widgets">
            <a href={props.link}>{props.title}</a>
        </div>
    );
}

export default HomepageDashboardHeader;