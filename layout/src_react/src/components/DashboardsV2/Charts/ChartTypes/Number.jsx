import React, { Component } from 'react'

class Number extends Component {

    constructor(props) {
        super(props)

        this.state = {
            value: 0
        }
    }


    componentDidMount() {
        if (this.props.yAxisTitle.toLowerCase() === 'sales' || this.props.yAxisTitle.toLowerCase() === 'aov') {
            const numberFormat = new Intl.NumberFormat('us-en', { style: 'currency', currency: 'usd' })
            this.setState({
                value: numberFormat.format(this.props.chartData[0][this.props.yFieldName])
            })
        }
        else {
            this.setState({
                value: this.props.chartData[0][this.props.yFieldName]
            })
        }
    }

    render() {
        return (
            <div>
                <h4 className="mt-4 font-weight-bold" style={{ fontSize: '12px', color: '#666' }} >{this.props.title}</h4>
                <p style={{ fontSize: '2.3rem', position: 'absolute', top: '35%', left: '0', right: '0' }} className="text-dark">{this.state.value}</p>
            </div>
        )
    }
}
export default Number;