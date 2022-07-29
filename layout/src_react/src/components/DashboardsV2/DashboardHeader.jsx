import React, { Component, Fragment } from 'react';
import NewChartModal from './Charts/NewChartModal/NewChartModal'
import DashSideMenu from './Charts/DashSideMenu/DashSideMenu';
import NewDashModal from './Charts/DashSideMenu/NewDashModal';
import RenameDashModal from './Charts/DashSideMenu/RenameDashModal';
import DeleteDashModal from './Charts/DashSideMenu/DeleteDashModal';


class DashboardHeader extends Component {

	constructor(props) {
		super(props);
		this.state = {
			name: props.dashName,
			modals: {
				newChart: { open: false },
				addDash: { open: false },
				renameDash: { open: false },
				deleteDash: { open: false }
			}
		}
		this.renameDash = this.renameDash.bind(this)
	}

	setModalState(modalName, state) {
		this.setState({
			modals: {
				...this.state.modals,
				[modalName]: { open: state }
			}
		}
		)
	}

	openModal(modalName) {
		this.setModalState(modalName, true)
	}

	closeModal(modalName) {
		this.setModalState(modalName, false)
	}

	renameDash(name) {
		this.setState({ name })
	}


	render() {
		return (
			<Fragment>
				<DashSideMenu openModal={name => this.openModal(name)} />
				<NewDashModal userId={this.props.defaultDashboard.user} _loadDashboardList={this.props._loadDashboardList} closeFunc={() => this.closeModal('addDash')} isOpen={this.state.modals.addDash.open} reloadDashboardFunc={this.props.reloadDashboardFunc} />
				<RenameDashModal _loadDashboardList={this.props._loadDashboardList} currentName={this.state.name} renameDash={this.renameDash} dashboardId={this.props.dashboardId} closeFunc={() => this.closeModal('renameDash')} isOpen={this.state.modals.renameDash.open} />
				<DeleteDashModal dashboardId={this.props.dashboardId} closeFunc={() => this.closeModal('deleteDash')} isOpen={this.state.modals.deleteDash.open} dashboardsList={this.props.dashboardsList} dashboardId={this.props.dashboardId} />
				<NewChartModal
					dashboardId={this.props.dashboardId}
					isOpen={this.state.modals.newChart.open}
					closeFunc={() => this.closeModal('newChart')}
					getNewChartLayoutFunc={this.props.getNewChartLayoutFunc}
					reloadDashboardFunc={this.props.reloadDashboardFunc}
				/>
				<div className="dash-header-menu">
					<div className="dropdown">
						<button className="btn btn-light btn-secondary dropdown-toggle" type="button" id="dropdownMenu2" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
							{this.state.name}
						</button>
						<div className="dropdown-menu bg-light dash-header-dropdown" aria-labelledby="dropdownMenu2">
							{this.props.dashboardsList && this.props.dashboardsList.map((dash, i) => <a href={`/dashboards/v2/${dash.id}/`} key={i} className="dropdown-item text-dark" type="button">{dash.name}</a>)}
						</div>
					</div>
					<button onClick={() => this.openModal('newChart')} className="btn_orange add-chart-btn" style={{ borderRadius: '20px', height: '35px' }}><i className="fa fa-plus"></i> <span>Add Metric</span></button>
				</div>
			</Fragment >
		)
	}
}

export default DashboardHeader;
