import React, { Component } from 'react'
import chartsImagesPaths from './ChartImagePaths'
import { getPredefinedMetrics } from '../../../../api/BLApi'

class MetricStep extends Component {
  constructor(props) {
    super(props);
    this.state = {
      predefinedMetrics: null
    }
  }

  componentDidMount() {

    getPredefinedMetrics(this.props.selectedOptions.integrations.map(i=>i.name)).then(predefinedMetrics => {
      console.log(predefinedMetrics)
      this.setState({
        predefinedMetrics: predefinedMetrics,
      })
    });
  }

  render() {
    return (
      <>
        <h4 style={{ opacity: '0.8' }}>What information do you want to see?</h4>
        <div className="d-flex flex-row mt-4 flex-wrap justify-content-center metric_item_container">
          {
            this.state.predefinedMetrics && this.state.predefinedMetrics.map(metric => (
              // TODO: it should be camell case: metric.chartType
              <div onClick={() => this.props.selectValueFunc(metric)} key={metric.name} className={"d-fex flex-column justify-content-center align-items-center " + (((this.props.selectedValue && metric.name == this.props.selectedValue.name)) ? 'border-yellow ' : '') + (false ? 'metric_item_google' : 'metric_item')}>
                <img width={35} height={35} src={chartsImagesPaths[metric.chart_type_icon.name]} />
                <p className="text-capitalize mt-2">{metric.name}</p>
              </div>
            ))
          }
        </div>
      </>
    )
  }

}

export default MetricStep;
