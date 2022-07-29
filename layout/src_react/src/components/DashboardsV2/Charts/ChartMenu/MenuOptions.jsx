import React, { Component, Fragment } from 'react'
import FavoriteModal from './FavoriteModal';
import EditModal from './EditModal';
import DeleteModal from './DeleteModal';


class MenuOptions extends Component {

	constructor(props) {
		super(props);
		this.state = {
			modals: {
				favorite: { open: false },
				edit: { open: false },
				delete: { open: false }
			}
		}
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

	render() {
		return (
			<Fragment>
				{(this.state.modals.favorite.open) && (
					<FavoriteModal
						{...this.props}
						isOpen={this.state.modals.favorite.open}
						closeFunc={() => this.closeModal('favorite')}
					/>)}
				{(this.state.modals.edit.open) && (
					<EditModal
						{...this.props}
						isOpen={this.state.modals.edit.open}
						closeFunc={() => this.closeModal('edit')}
					/>)}
				{(this.state.modals.delete.open) && (
					<DeleteModal
						isOpen={this.state.modals.delete.open}
						closeFunc={() => this.closeModal('delete')}
						chartId={this.props.chartId}
						removeChartFromGridLayoutFunc={this.props.removeChartFromGridLayoutFunc}
					/>)}

				<div className="dropdown">
					<button style={{ background: '#fff', border: 'none' }} className="btn btn-light" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
						<i style={{ width: '50px', position: 'absolute', right: '-10px', top: '10px' }} className="fa fa-ellipsis-v"></i>
					</button>
					<div style={{ fontSize: '14px', cursor: 'pointer' }} className="dropdown-menu dropdown-menu-right bg-light" aria-labelledby="dropdownMenuButton">
						<a key={1} onClick={() => this.openModal('favorite')} className="dropdown-item">Favorite</a>
						<a key={2} onClick={() => this.openModal('edit')} className="dropdown-item">Edit</a>
						<a key={3} onClick={() => this.openModal('delete')} className="dropdown-item">Delete</a>
					</div>
				</div>
			</Fragment>
		)
	}
}

export default MenuOptions;
