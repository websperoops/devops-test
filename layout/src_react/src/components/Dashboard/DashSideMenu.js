import React from 'react'
import DashSideMenuItem from './DashSideMenuItem';
import "./dashSideMenu.css";

const DashSideMenu = ({ showSideBar, closeSideBar, enableRenameModal, enableResetModal, enableNewDashModal, enableDeleteDashModal }) => {

    const handleMouseEnter = () => {
        document.querySelector('.dash-header-dropdown').classList.remove('show')
        document.querySelector('.profile-dropdown').classList.remove('show')

    }

    return (
        <ul onMouseEnter={handleMouseEnter} className={showSideBar ? 'dash-side-menu dash-side-menu-open' : 'dash-side-menu'}>
            <i onClick={closeSideBar} className="fa fa-times close-icon"></i>
            <DashSideMenuItem enableNewDashModal={enableNewDashModal && enableNewDashModal} icon="fa fa-plus" text="New Dashboard" />
            <DashSideMenuItem enableRenameModal={enableRenameModal && enableRenameModal} icon="fa fa-pencil" text="Rename" />
            <DashSideMenuItem enableDeleteDashModal={enableDeleteDashModal && enableDeleteDashModal} icon="fa fa-times" text="Delete" />
            <DashSideMenuItem enableResetModal={enableResetModal && enableResetModal} modal="#resetDashModal" icon="fa fa-undo" text="Reset Layout" />
        </ul >
    )
}

export default DashSideMenu;