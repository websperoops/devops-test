import React, { Component } from 'react'
import { getIntegrationsList } from '../../api/BLApi';
import MenuOptions from './Charts/ChartMenu/MenuOptions';


class DashWidgetTopPanel extends Component {

  constructor(props) {
    super(props);

    this.state = {
      integrations: []
    }
  }

  componentDidMount() {
    getIntegrationsList().then(data => {
      data.forEach(item => {
        if (item.id === this.props.integrations_id[0]) {
          this.setState({ integrations: [item.name] })
        }
      })
    })
  }

  render() {
    return (
      <div className="menu" id={this.props.id + "_menu"}>
        <h5 class="d-flex flex-row align-items-center"> <img className="mr-2" width="30" src={this.state.integrations[0] && `/static/images/${this.state.integrations[0]}-icon.png`} /> {this.props.chartName}</h5>
        <div className="graph-menu-icons">
          <MenuOptions
            {...this.props}
          />
        </div>
      </div>
    )
  }
}

export default DashWidgetTopPanel;
