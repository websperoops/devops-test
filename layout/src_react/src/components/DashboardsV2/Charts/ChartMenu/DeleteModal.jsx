import React, { Component } from 'react'
import ReactModal from 'react-modal'
import { deleteChart } from '../../../../api/BLApi'


class DeleteModal extends Component {

  constructor(props) {
    super(props);

    this.handleDelete = this.handleDelete.bind(this);
  }

  handleDelete() {
    deleteChart(this.props.chartId)
      .then(this.props.removeChartFromGridLayoutFunc(this.props.chartId))
      .catch(err => console.error(err))
    this.props.closeFunc();
  }

  render() {
    return (
      <ReactModal
        onRequestClose={this.props.closeFunc}
        className="modal-outer"
        isOpen={this.props.isOpen}
        shouldCloseOnEsc={true}
        shouldCloseOnOverlayClick={true}
        ariaHideApp={false}
      >
        <div className="modal-inner">
          <h3 style={{ fontSize: '20px' }}>Delete this Metric?</h3>
          <div className="d-flex flex-row justify-content-center">
            <button onClick={this.handleDelete} className="btn_orange">Yes</button>
            <button onClick={this.props.closeFunc} className="btn_clear">No</button>
          </div>
        </div>
      </ReactModal>
    )
  }
}

export default DeleteModal;
