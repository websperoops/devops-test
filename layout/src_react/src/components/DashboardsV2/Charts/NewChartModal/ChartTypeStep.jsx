import React, { Component } from 'react'
import chartsImagesPaths from './ChartImagePaths'
import { getPredefinedChartTypes } from '../../../../api/BLApi'

class ChartTypeStep extends Component {

  constructor(props) {
    super(props);
    this.state = {
      predefinedChartTypes: null
    }
  }

  componentDidMount() {
    getPredefinedChartTypes(this.props.selectedOptions.metric.id).then(predefinedChartTypes => {
      console.log(predefinedChartTypes)
      this.setState({
        predefinedChartTypes: predefinedChartTypes,
      })
    });
  }

  render() {
    return (
      <>
        <h4 style={{ opacity: '0.8' }}>Select chart type</h4>

        <div className="d-flex flex-row mt-4 flex-wrap justify-content-center type_item_container">
          {this.state.predefinedChartTypes && this.state.predefinedChartTypes.map(chartType => {
            return (
              <div
                key={chartType.name}
                onClick={() => this.props.selectValueFunc(chartType)}
                className={"account_item d-fex flex-column justify-content-center align-items-center " + ((this.props.selectedValue && (this.props.selectedValue.name == chartType.name)) ? 'border-yellow' : '')}
              >
                <img className='mx-auto' width={35} height={35} src={chartsImagesPaths[chartType.name]} />
                <p className="text-capialize mt-2">{chartType.name.replace(/_/g, ' ')}</p>
              </div>
            )
          })}
        </div>
      </>
    )
  }
}

export default ChartTypeStep;
