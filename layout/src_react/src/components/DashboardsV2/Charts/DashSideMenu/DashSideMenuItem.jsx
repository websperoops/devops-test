import React, { Component } from 'react'

class DashSideMenuItem extends Component {
    render() {
        return (
            <li data-toggle="modal" onClick={this.props.handleOpenModal}>
                <i className={this.props.icon} style={{ marginRight: '5px' }}></i>
                <p className={this.props.showBar && 'show-icon-text'}>{this.props.text}</p>
            </li >
        )
    }

}

export default DashSideMenuItem;