import React, { Component } from 'react'
import DashSideMenuItem from './DashSideMenuItem';

class DashSideMenu extends Component {
    render() {
        return (
            <>
                <ul className='dash-side-menu' onMouseEnter={() => {
                    document.querySelector('.dash-header-dropdown').classList.remove('show')
                    document.querySelector('.profile-dropdown').classList.remove('show')
                }}>
                    <i className="fa fa-times close-icon"></i>
                    <DashSideMenuItem handleOpenModal={() => this.props.openModal('addDash')} {...this.props} icon="fa fa-plus" text="New Dashboard" />
                    <DashSideMenuItem handleOpenModal={() => this.props.openModal('renameDash')} {...this.props} icon="fa fa-pencil" text="Rename" />
                    <DashSideMenuItem handleOpenModal={() => this.props.openModal('deleteDash')} {...this.props} icon="fa fa-times" text="Delete" />
                    <DashSideMenuItem handleOpenModal={() => this.props.openModal('resetDash')} {...this.props} icon="fa fa-undo" text="Reset Layout" />
                </ul >
            </>
        )
    }
}

export default DashSideMenu;