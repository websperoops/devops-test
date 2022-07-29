import React, { useState, useEffect } from 'react'
import DashSideMenu from './DashSideMenu';
import NewChartModal from './NewChartModal';
import RenameDashModal from './RenameDashModal';
import DashResetModal from './DashResetModal';
import DashCreateModal from './DashCreateModal';
import DashDeleteModal from './DashDeleteModal';
import NewChartForm from '../MultiStepForms/NewChartForm/NewChartForm'


function DashHeaderMenu(props) {
    const [current, setCurrent] = useState();
    const [dashId, setDashId] = useState();
    const [showSideBar, setShowSideBar] = useState(false);
    const [showAddChart, setShowAddChart] = useState(false)
    const [showRenameModal, setShowRenameModal] = useState(false)
    const [showResetModal, setShowResetModal] = useState(false)
    const [showNewDashModal, setShowNewDashModal] = useState(false);
    const [showDeleteDashModal, setShowDeleteDashModal] = useState(false);
    const handleDashChange = (e) => window.location.href = `/dashboards/${e.target.value}/view`


    useEffect(() => {
        dashboards.map(dash => {
            if (window.location.href.indexOf(dash.id) > -1) {
                setDashId(dash.id)
                setCurrent(decodeURI(dash.title))
            }
        })

    }, [dashboards])

    const dashChange = id => window.location.href = `/dashboards/${id}/view`
    const handleCloseSidebar = () => setShowSideBar(false);
    const handleCloseAddChartModal = () => setShowAddChart(false);
    const handleCloseRenameDashModal = () => setShowRenameModal(false)
    const handleCloseResetModal = () => setShowResetModal(false);
    const handleCloseNewDashModal = () => setShowNewDashModal(false);
    const handleCloseDeleteDashModal = () => setShowDeleteDashModal(false);

    useEffect(() => {
        if (showRenameModal) {
            setShowDeleteDashModal(false);
            setShowNewDashModal(false)
            setShowResetModal(false)
            setShowSideBar(false)
        }

        else if (showDeleteDashModal) {
            setShowRenameModal(false);
            setShowNewDashModal(false)
            setShowResetModal(false)
            setShowSideBar(false)

        }

        else if (showResetModal) {
            setShowRenameModal(false);
            setShowNewDashModal(false)
            setShowDeleteDashModal(false)
            setShowSideBar(false)

        }
        else if (showNewDashModal) {
            setShowRenameModal(false);
            setShowResetModal(false)
            setShowDeleteDashModal(false)
            setShowSideBar(false)

        }
    }, [showDeleteDashModal, showNewDashModal, showRenameModal, showResetModal])

    return (
        <div className="dash-header-menu">
            <i className="fa fa-bars" onClick={() => setShowSideBar(true)}></i>
            <div className="dropdown">
                <button className="btn btn-light btn-secondary dropdown-toggle" type="button" id="dropdownMenu2" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    {unescape(current)}
                </button>
                <div className="dropdown-menu bg-light dash-header-dropdown" aria-labelledby="dropdownMenu2">
                    {dashboards.map(dash => <button onClick={() => dashChange(dash.id)} key={dash.id} className="dropdown-item text-dark" type="button">{unescape(dash.title)}</button>)}
                </div>
            </div>
            <DashSideMenu
                enableResetModal={() => setShowResetModal(true)}
                enableRenameModal={() => setShowRenameModal(true)}
                enableNewDashModal={() => setShowNewDashModal(true)}
                enableDeleteDashModal={() => setShowDeleteDashModal(true)}
                showSideBar={showSideBar}
                closeSideBar={handleCloseSidebar} />
            <NewChartForm show={showAddChart} dashId={dashId} close={handleCloseAddChartModal} />
            {/* <NewChartModal show={showAddChart} close={handleCloseAddChartModal} dashId={dashId} /> */}

            <RenameDashModal show={showRenameModal} close={handleCloseRenameDashModal} dashId={dashId} currentName={current} />
            <DashResetModal show={showResetModal} close={handleCloseResetModal} dashId={dashId} />
            <DashCreateModal show={showNewDashModal} close={handleCloseNewDashModal} />
            <DashDeleteModal show={showDeleteDashModal} close={handleCloseDeleteDashModal} />
            <button onClick={() => setShowAddChart(true)} className="btn_orange add-chart-btn" style={{borderRadius: '20px', height: '35px'}}><i className="fa fa-plus"></i> <span>Add Metric</span></button>
        </div>
    )
}

export default DashHeaderMenu;