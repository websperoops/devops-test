import React from 'react'
import DashSideMenuText from './DashSideMenuText';
import "./dashSideMenu.css";

const DashSideMenuItem = props => {
    const showModal = () => {
        switch (props.text) {
            case 'Rename':
                props.enableRenameModal();
            case 'Reset Layout':
                props.enableResetModal();
            case 'New Dashboard':
                props.enableNewDashModal();
            case 'Delete':
                props.enableDeleteDashModal();
            default:
                return null;
        }
    }
    return (
        <li data-toggle="modal" href={props.modal} onClick={showModal}>
            <i className={props.icon} style={{ marginRight: '5px' }}></i>
            <DashSideMenuText showBar={props.showBar} text={props.text} />
        </li >
    )
}

export default DashSideMenuItem;