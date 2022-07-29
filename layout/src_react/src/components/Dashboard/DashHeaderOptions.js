import React from 'react'

function DashHeaderOptions(props) {
    return (
        <ul className="dash-header-options">
            <li data-toggle="modal" href="#newDashboardModal"><i className="fa fa-plus"></i>New</li>
            <li href="#renameDashModal" data-toggle="modal"><i className="fa fa-pencil"></i>Rename</li>
            {/* <li data-toggle="modal" href="#defaultDashModal"><i class="fa fa-star"></i>Favorite</li> */}
            <li data-toggle="modal" href="#deleteDashModal"><i className="fa fa-times"></i>Delete</li>
            <li data-toggle="modal" href="#resetDashModal"><i className="fa fa-undo"></i>Reset</li>
        </ul>
    )
}

export default DashHeaderOptions;