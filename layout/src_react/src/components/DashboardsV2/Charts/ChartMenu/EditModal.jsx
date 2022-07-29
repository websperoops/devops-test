import React, { Component } from 'react'
import ReactModal from 'react-modal'
import chartsIconsPaths from '../NewChartModal/ChartImagePaths'
import { getChartTypeId, getPredefinedMetricTypes, getPredefinedChartTypes, getPredefinedTimeRanges, editMetric, editTimeRange } from '../../../../api/BLApi';
import "../../../Dashboard/dashMainPage.css";

class EditModal extends Component {

  constructor(props) {
    super(props);

    this.state = {
      predefinedMetricTypes: null,
      selectedData: null,
      predefinedChartTypes: null,
      selectedChartTypeId: null,
      selectedChartTypeName: null,
      predefinedTimeRanges: null,
      selectedTimeRange: null,
    }
    this.handleEditChart = this.handleEditChart.bind(this);
  }

  componentDidMount() {
    getPredefinedMetricTypes(this.props.premetricId).then(predefinedMetricTypes => {
      console.log(predefinedMetricTypes)
      this.setState({
        predefinedMetricTypes: predefinedMetricTypes,
      })
      //set initial state value. This is needed when using <select> with first default option
      const current = predefinedMetricTypes.find(type => this.props.chartName.includes(type.name))
      current ? this.setState({ selectedData: current.id }) : this.state.predefinedMetricTypes !== null && this.setState({ selectedData: predefinedMetricTypes[0].id })
    });

    getPredefinedChartTypes(this.props.premetricId).then(predefinedChartTypes => {
      this.setState({
        predefinedChartTypes: predefinedChartTypes,
      })

      this.state.predefinedChartTypes && this.setState({ selectedChartType: this.state.predefinedChartTypes[0] })
    });

    getPredefinedTimeRanges(this.props.premetricId).then(predefinedTimeRanges => {
      this.setState({
        predefinedTimeRanges: predefinedTimeRanges,
      })
      //set initial state value. This is needed when using <select> with first default option
      this.state.predefinedTimeRanges && this.setState({ selectedTimeRange: this.state.predefinedTimeRanges[0].id })
    });

  }

  handleGetChartTypeId(name) {
    getChartTypeId(name).then(data => this.setState({
      selectedChartTypeId: data.results[0].id,
      selectedChartTypeName: name
    }))
  }

  handleEditChart() {
    let chartData = new Object({ metric: {} });
    if (this.state.predefinedMetricTypes !== null) {
      const metricIndex = this.state.predefinedMetricTypes.findIndex(c => c.id == Number(this.state.selectedData))
      const metric = this.state.predefinedMetricTypes[metricIndex]
      chartData.metric.name = metric.name
      chartData.metric.title = metric.title
      chartData.metric.filter = metric.filter_expression
      chartData.metric.group_by = metric.group_by_expression
      chartData.metric.aggregate = metric.aggregate_expression
      chartData.metric.x_field = metric.x_field
      chartData.metric.y_field = metric.y_field
      chartData.metric.group_field = metric.group_field
      chartData.metric.x_label = metric.x_label
      chartData.metric.y_label = metric.y_label
      chartData.metric.group_label = metric.group_label
      chartData.metric.datasource = metric.datasource
      chartData.metric.chart_type_id = this.state.selectedChartTypeId
    }

    const chosenTime = this.state.predefinedTimeRanges.find(time => time.id == this.state.selectedTimeRange);
    Promise.all([
      editMetric(chartData, this.props.metricId),
      chosenTime && editTimeRange(this.props.time_range_id, { since: chosenTime.since, until: chosenTime.until })
    ]).then(
      () => this.props.loadChartData([this.props.chartId])
    ).catch(error => console.error(error))
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
        <div className="modal-inner edit-metric-modal">
          <h3>Edit Metric</h3>
          <div className="d-flex flex-column justify-content-center edit-metric-container mt-3">
            <div className="d-flex flex-column justify-content-center">
              <div className="edit-metric-header-container">
                <p className="text-left ml-2 mt-1">Data</p>
              </div>
              <div className="d-flex flex-column justify-content-center">
                <p>What information do you wish to see?</p>
                <select style={{ width: '250px' }} disabled={this.state.predefinedMetricTypes == null} className="mx-auto mb-3" value={this.state.selectedData && this.state.selectedData} onChange={e => this.setState({ selectedData: e.target.value })}>
                  {this.state.predefinedMetricTypes !== null && this.state.predefinedMetricTypes.map(o => <option key={o.id} value={o.id}>{o.name}</option>)}
                </select>
              </div>
            </div>

            <div className="d-flex flex-column justify-content-center">
              <div className="edit-metric-header-container">
                <p className="text-left ml-2 mt-1">Type</p>
              </div>
              <div className="d-flex flex-row mt-4 flex-wrap justify-content-center">
                {this.state.predefinedChartTypes && this.state.predefinedChartTypes.map(c => (
                  <div key={c.id} onClick={() => this.handleGetChartTypeId(c.name)} className={"edit_type_item d-fex flex-column justify-content-center align-items-center mb-3 " + (this.state.selectedChartTypeName && this.state.selectedChartTypeName == c.name ? 'border-yellow' : '')}>
                    <img className='mx-auto' width={35} height={35} src={chartsIconsPaths[c.name] || null} />
                    <p className="text-capialize mt-2">{c.name.replace(/_/g, ' ')}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="d-flex flex-column justify-content-center">
              <div className="edit-metric-header-container">
                <p className="text-left ml-2 mt-1">Time</p>
              </div>
              <div className="d-flex flex-column justify-content-center">
                <select disabled={this.state.predefinedTimeRanges == null || this.state.predefinedTimeRanges.length === 0} className="mx-auto mb-3" value={this.state.selectedTimeRange && this.state.selectedTimeRange.name} onChange={e => this.setState({ selectedTimeRange: Number(e.target.value) })}>
                  {this.state.predefinedTimeRanges !== null && this.state.predefinedTimeRanges.length ? this.state.predefinedTimeRanges.map(o => <option key={o.id} value={o.id}>{o.name}</option>) : <option>N/A</option>}
                </select>
              </div>
            </div>
          </div>
          <div className="d-flex flex-row justify-content-end">
            <button onClick={this.props.closeFunc} className="btn_clear">Close</button>
            <button onClick={this.handleEditChart} className="btn_orange">Save</button>
          </div>
        </div>
      </ReactModal >
    )
  }
}

export default EditModal;
