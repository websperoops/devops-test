import React, { Component } from 'react'
import ReactModal from 'react-modal'
//import { addFreshChart } from '../../Dashboard';
import AccountStep from './AccountStep'
import MetricStep from './MetricStep'
import MetricTypeStep from './DataStep'
import ChartTypeStep from './ChartTypeStep'
import TimeRangeStep from './TimeRangeStep'
import { addChart } from '../../../../api/BLApi'

class NewChartModal extends Component {

  constructor(props) {
    super(props);
    this.state = {
      currentStep: 0,
      selectedOptions: {
        integrations: null,
        metric: null,
        metricType: null,
        chartType: null,
        timeRange: null,
      }
    }

    this.selectValueWrapper = this.selectValueWrapper.bind(this)
    this.handleOneStepBack = this.handleOneStepBack.bind(this)
    this.handleOneStepNext = this.handleOneStepNext.bind(this)
    this.handleAddChart = this.handleAddChart.bind(this)
    this.resetSteps = this.resetSteps.bind(this)

    // NOTE: This needs to be after bounding the functions (because they are used here)
    this.steps = [
      {
        _class: AccountStep,
        valueName: 'integrations',
        valueFunc: this.selectValueWrapper('integrations'),
      },
      {
        _class: MetricStep,
        valueName: 'metric',
        valueFunc: this.selectValueWrapper('metric'),
      },
      {
        _class: MetricTypeStep,
        valueName: 'metricType',
        valueFunc: this.selectValueWrapper('metricType'),
      },
      {
        _class: ChartTypeStep,
        valueName: 'chartType',
        valueFunc: this.selectValueWrapper('chartType'),
      },
      {
        _class: TimeRangeStep,
        valueName: 'timeRange',
        valueFunc: this.selectValueWrapper('timeRange'),
      },
    ]


  }

  selectValueWrapper(valueName) {
    return (value) => {
      this.setState({
        selectedOptions: {
          ...this.state.selectedOptions,
          [valueName]: value
        }
      })
    }
  }

  handleOneStepBack() {
    this.setState((state, props) => ({
      currentStep: state.currentStep - 1,
    })
    )
  }

  handleOneStepNext() {
    this.setState((state, props) => ({
      currentStep: state.currentStep + 1,
    })
    )
  }

  handleAddChart() {
    let chartData = {
      "dashboard": Number(this.props.dashboardId),
      "metric": {
        "name": this.state.selectedOptions.metricType.name,
        "title": this.state.selectedOptions.metricType.title,
        "filter": this.state.selectedOptions.metricType.filter_expression,
        "group_by": this.state.selectedOptions.metricType.group_by_expression,
        "aggregate": this.state.selectedOptions.metricType.aggregate_expression,
        "time_group_by": this.state.selectedOptions.metricType.time_group_by_expression,
        "x_field": this.state.selectedOptions.metricType.x_field,
        "y_field": this.state.selectedOptions.metricType.y_field,
        "group_field": this.state.selectedOptions.metricType.group_field,
        "x_label": this.state.selectedOptions.metricType.x_label,
        "y_label": this.state.selectedOptions.metricType.y_label,
        "group_label": this.state.selectedOptions.metricType.group_label,
        "datasource": this.state.selectedOptions.metricType.datasource,
        "integrations": this.state.selectedOptions.integrations.map((i => i.id)),
        "chart_type": this.state.selectedOptions.chartType.name,
        "time_range": this.state.selectedOptions.timeRange && ({
          "since": this.state.selectedOptions.timeRange.since,
          "until": this.state.selectedOptions.timeRange.until
        }) || null,
      },
      "predefined_metric": this.state.selectedOptions.metric.id,
      "dashboard_layout": this.props.getNewChartLayoutFunc(),
    }

    addChart(chartData).then(data => {
      this.props.reloadDashboardFunc([data.id])
      this.props.closeFunc();
    }).catch((err) => { console.error(err) })
    this.resetSteps()

  }

  resetSteps() {
    this.setState({
      currentStep: 0,
      selectedOptions: {
        integration: null,
        metric: null,
        metricType: null,
        chartType: null,
        timeRange: null,
      }
    })
  }



  render() {
    let currentStep = this.steps[this.state.currentStep]
    let CurrentStepClass = currentStep._class
    let isNextEnabled = Boolean(this.state.selectedOptions[currentStep['valueName']])


    return (
      <ReactModal
        className="modal-outer multistep-form-modal"
        isOpen={this.props.isOpen}
        ariaHideApp={false}
        shouldCloseOnEsc={true}
        onRequestClose={this.props.closeFunc}
      >
        <div className="modal-inner">
          <h2 style={{ width: '90%' }} className="text-center">Add A New Metric</h2>
          <div>
            <div className="navigation-step d-flex flex-row justify-content-center mt-3 mb-3">
              <div className="navigation-step-item">Account</div>
              <div className={"navigation-step-item " + (this.state.currentStep > 0 ? 'navigation-step-item-complete' : null)}>Metric</div>
              <div className={"navigation-step-item " + (this.state.currentStep > 1 ? 'navigation-step-item-complete' : null)}>Data</div>
              <div className={"navigation-step-item " + (this.state.currentStep > 2 ? 'navigation-step-item-complete' : null)}>Type</div>
              <div className={"navigation-step-item " + (this.state.currentStep > 3 ? 'navigation-step-item-complete' : null)}>Time</div>
            </div>
            <CurrentStepClass selectedValue={this.state.selectedOptions[currentStep.valueName]} selectValueFunc={currentStep.valueFunc} selectedOptions={this.state.selectedOptions} />
          </div>
          <div className="d-flex flex-row justify-content-end mx-auto" style={{ width: '90%' }}>
            <button className="btn_clear" onClick={this.state.currentStep > 0 ? this.handleOneStepBack : this.props.closeFunc}>{this.state.currentStep > 0 ? 'Back' : 'Close'}</button>
            {(this.state.currentStep < 4) && <button disabled={!isNextEnabled} className={(!isNextEnabled ? 'btn_gray' : 'btn_orange')} onClick={this.handleOneStepNext}>Next</button>}
            {(this.state.currentStep == 4) && <button className="btn_orange" onClick={this.handleAddChart}>Finish</button>}
          </div>
        </div>
      </ReactModal >
    )
  }
}

export default NewChartModal
