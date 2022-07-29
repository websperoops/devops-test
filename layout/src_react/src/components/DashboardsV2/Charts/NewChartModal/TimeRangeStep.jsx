import React, { Component } from 'react'
import { getPredefinedTimeRanges } from '../../../../api/BLApi'

class TimeRangeStep extends Component {


	constructor(props) {
    super(props);
		this.state = {
			predefinedTimeRanges: null
		}
  }

	componentDidMount()	{
		getPredefinedTimeRanges(this.props.selectedOptions.metric.id).then(predefinedTimeRanges => {
			console.log(predefinedTimeRanges)
			this.setState({
				predefinedTimeRanges: predefinedTimeRanges,
			})
      //set initial state value. This is needed when using <select> with first default option
      this.props.selectValueFunc(predefinedTimeRanges[0])
		});
	}

  render() {
    return (
        <>
            <h4 style={{ opacity: '0.8' }}>Select a time period</h4>

            <div>
                <select
                  onChange={(event) => {console.log('___clicked__');this.props.selectValueFunc(this.state.predefinedTimeRanges.filter(o => o.id == event.target.value)[0])}}
                  disabled={!this.state.predefinedTimeRanges || (this.state.predefinedTimeRanges.length == 0)}>
                    { this.state.predefinedTimeRanges && (
                      (this.state.predefinedTimeRanges.length == 0)
                        ? <option>All Time</option>
                        : (
                          this.state.predefinedTimeRanges.map(timeRange => <option key={timeRange.id} value={timeRange.id}>{timeRange.name}</option>)
                        )
                    )}
                </select>
            </div>
        </>
    )
  }

}

export default TimeRangeStep;
