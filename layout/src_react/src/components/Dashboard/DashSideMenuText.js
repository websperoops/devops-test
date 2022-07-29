import React from 'react'
import "./dashSideMenu.css";

const DashSideMenuText = (props) => {
    return (
        <p className={props.showBar && 'show-icon-text'}>{props.text}</p>
    )
}

export default DashSideMenuText;