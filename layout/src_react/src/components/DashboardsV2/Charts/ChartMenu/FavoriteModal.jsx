import { get } from 'lodash';
import React, { Component } from 'react'
import ReactModal from 'react-modal'
import { getFavoriteDashboard, getChart, addChart, getDataSourceObj } from '../../../../api/BLApi';



class FavoriteModal extends Component {

  constructor(props) {
    super(props);
    this.favoritize = this.favoritize.bind(this);
  }

  favoritize() {
    Promise.all([getFavoriteDashboard(), getChart(Number(this.props.chartId))])
      .then(values => {
        getDataSourceObj(values[1].metric.datasource).then(res => {
          const chartData = {
            dashboard: values[0].id,
            metric: {
              ...values[1].metric,
              chart_type: values[1].metric.chart_type.name,
              datasource: res.results[0].id,
            },
            predefined_metric: values[1].predefined_metric.id,
            dashboard_layout: this.props.getNewChartLayoutFunc()
          }
          addChart(chartData).then(data => {
            this.props.closeFunc();
          }).catch((err) => { console.error(err) })
        });

      })
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
          <h3 style={{ fontSize: '20px' }}>Favorite this Metric?</h3>
          <div className="d-flex flex-row justify-content-center">
            <button onClick={this.favoritize} className="btn_orange">Yes</button>
            <button onClick={this.props.closeFunc} className="btn_clear">No</button>
          </div>
        </div>
      </ReactModal>
    )
  }
}

export default FavoriteModal;
