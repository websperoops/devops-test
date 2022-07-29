import React, { Component } from 'react'
import { getPredefinedMetricTypes } from '../../../../api/BLApi'

class MetricTypeStep extends Component {

	constructor(props) {
    super(props);
		this.state = {
			predefinedMetricTypes: null
		}
  }

	componentDidMount()	{

		getPredefinedMetricTypes(this.props.selectedOptions.metric.id).then(predefinedMetricTypes => {
			console.log(predefinedMetricTypes)
			this.setState({
				predefinedMetricTypes: predefinedMetricTypes,
			})
      //set initial state value. This is needed when using <select> with first default option
      this.props.selectValueFunc(predefinedMetricTypes[0])
		});
	}

  render() {

    return (
        <>
            <h4 style={{ opacity: '0.8' }}>What information do you wish to see?</h4>
            <div>
              {
                ((!this.state.predefinedMetricTypes || this.state.predefinedMetricTypes && (this.state.predefinedMetricTypes.length == 0)))
                && (
                  <select style={{ width: '300px' }} disabled={true}>
                      <option>Select a data option:</option> : <option>N/A</option>
                  </select>
                ) || (
                  <select onChange={(event) => {console.log('___clicked__');this.props.selectValueFunc(this.state.predefinedMetricTypes.filter(o => o.id == event.target.value)[0])}} style={{ width: '300px' }}>
                      {this.state.predefinedMetricTypes.map(metricType => <option key={metricType.id} value={metricType.id}>{metricType.name}</option>)}
                  </select>
                )
              }
            </div>

        </>
    )
  }
}

export default MetricTypeStep;
