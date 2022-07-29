import React, { Fragment, useState, useEffect } from 'react'
import EditModal from './EditModal';
import FavoriteModal from './FavoriteModal';
import DeleteChartModal from './DeleteChartModal';
import RateMetricModal from './RateMetricModal'
import "./dashMainPage.css";

function DashActionMenu(props) {
    const [showEditModal, setEditModal] = useState(false);
    const [showFaveModal, setFaveModal] = useState(false);
    const [showDeleteModal, setDeleteModal] = useState(false);
    const [showRateModal, setRateModal] = useState(false);


    function handleChange(val) {
        switch (val) {
            case 'Edit':
                setEditModal(true);
                return;
            case 'Rate':
                setRateModal(true)
                return;
            case 'Delete':
                setDeleteModal(true);
                return;
            case 'Favorite':
                setFaveModal(true);
                return;
            default:
                return;
        }
    }

    return (
        <Fragment>
            {showEditModal && <EditModal show={showEditModal} id={props.id} chart={props.chart} close={() => setEditModal(false)} />}
            {showFaveModal && <FavoriteModal show={showFaveModal} id={props.id} close={() => setFaveModal(false)} />}
            {showDeleteModal && <DeleteChartModal show={showDeleteModal} id={props.id} close={() => setDeleteModal(false)} />}
            {showRateModal && <RateMetricModal show={showRateModal} id={props.id} close={() => setRateModal(false)} />}


            <div className="dropdown">
                <button className="btn btn-light btn-dropdown-dashActionMenu" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <i className="fa fa-ellipsis-v icon-dropdown-dashActionMenu"></i>
                </button>
                <div style={{ fontSize: '14px', cursor: 'pointer' }} className="dropdown-menu dropdown-menu-right bg-light" aria-labelledby="dropdownMenuButton">
                    <a onClick={() => handleChange('Favorite')} className="dropdown-item">Favorite</a>
                    <a onClick={() => handleChange('Edit')} className="dropdown-item">Edit</a>
                    <a onClick={() => handleChange('Rate')} className="dropdown-item">Rate</a>
                    <a onClick={() => handleChange('Delete')} className="dropdown-item">Delete</a>

                </div>
            </div>

        </Fragment>
    )
}

export default DashActionMenu;