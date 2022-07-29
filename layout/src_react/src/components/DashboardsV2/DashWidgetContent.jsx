import React, { Component } from 'react'
import LineChart from './Charts/ChartTypes/LineChart';
import ColumnChart from './Charts/ChartTypes/ColumnChart'
import PieChart from './Charts/ChartTypes/PieChart'
import AreaChart from './Charts/ChartTypes/AreaChart'
import StackedColumnChart from './Charts/ChartTypes/StackedColumnChart'
import DualAxisChart from './Charts/ChartTypes/DualAxisChart'
import USAMapChart from './Charts/ChartTypes/USAMapChart'
import ScatterPlotChart from './Charts/ChartTypes/ScatterPlotChart'
import AreaSplineChart from './Charts/ChartTypes/AreaSplineChart'
import PackedBubbleChart from './Charts/ChartTypes/PackedBubbleChart';
import FunnelChart from './Charts/ChartTypes/FunnelChart';
import BellCurveChart from './Charts/ChartTypes/BellCurveChart';
import HistogramChart from './Charts/ChartTypes/HistogramChart';
import SankeyDiagram from './Charts/ChartTypes/SankeyDiagram';
import WordCloudChart from './Charts/ChartTypes/WordCloudChart';
import HeatMapChart from './Charts/ChartTypes/HeatMap';
import DumbellChart from './Charts/ChartTypes/DumbellChart';
import BarChart from './Charts/ChartTypes/BarChart';
import Table from './Charts/ChartTypes/DataTable';
import Number from './Charts/ChartTypes/Number'
import Treemap from './Charts/ChartTypes/Treemap';
import WorldMap from './Charts/ChartTypes/WorldMap'


class DashWidgetContent extends Component {
  constructor(props) {
    super(props);
    this.chartTypesMapping = {
      'Line': LineChart,
      'Column': ColumnChart,
      'Pie': PieChart,
      'Area': AreaChart,
      'Stacked_Column': StackedColumnChart,
      'Stacked_Column_%': StackedColumnChart,
      'Dual_Axis': DualAxisChart,
      'USA_Map': USAMapChart,
      'Bar': BarChart,
      'Stacked_Bar': BarChart,
      'Area_Spline': AreaSplineChart,
      'Scatter_Plot': ScatterPlotChart,
      'Funnel': FunnelChart,
      'Packed_Bubble': PackedBubbleChart,
      'Histogram': HistogramChart,
      'Bell_Curve': BellCurveChart,
      'Sankey_Diagram': SankeyDiagram,
      'Word_Cloud': WordCloudChart,
      'Heat_Map': HeatMapChart,
      'Dumbell': DumbellChart,
      'Table': Table,
      'Number': Number,
      'Tree_Map': Treemap,
      'World_Map': WorldMap
    }
    this.chartStylesMapping = {
      'Line': 'h-100',
      'Column': 'h-100',
      'Pie': 'h-100',
      'Area': 'h-100',
      'Stacked_Column': 'h-100',
      'Stacked_Column_%': 'h-100',
      'Dual_Axis': 'h-100',
      'USA_Map': 'h-100',
      'Bar': 'h-100',
      'Stacked_Bar': 'h-100',
      'Area_Spline': 'h-100',
      'Scatter_Plot': 'h-100',
      'Funnel': 'h-100',
      'Packed_Bubble': 'h-100',
      'Histogram': 'h-100',
      'Bell_Curve': 'h-100',
      'Sankey_Diagram': 'h-100',
      'Word_Cloud': 'h-100',
      'Heat_Map': 'h-100',
      'Dumbell': 'h-100',
      'Table': 'tableContainer', // important line to alternate
      'Number': 'chartContainer',
      'Tree_Map': 'h-100',
      'World_Map': 'h-100'
    }
  }

  render() {
    if (!this.props.chartType) {
      console.error('ChartType: ' + String(this.props.chartType))
      return <div />
    }
    if (!Object.keys(this.chartTypesMapping).map(t => t.toLowerCase()).includes(this.props.chartType.toLowerCase())) {
      console.error("Unknown chart type: " + String(this.props.chartType))
      return <div />
    }

    let DynamicChartType = this.chartTypesMapping[this.props.chartType]
    return (
      <div className="grid-stack-item-content" style={{ visibility: "unset", position: 'relative', height: this.props.chartType == 'Table' ? 'calc(100% - 80px)' : '100%' }}>
        {/* In liu of className h-100 */}
        <div className="widget h-100">
          <div className={`widget-content ${this.chartStylesMapping[this.props.chartType]} tight-container`} style={{ backgroundColor: "transparent", marginTop: "0", overflowY: this.props.chartType == 'Table' ? 'scroll' : 'hidden' }}>
            <DynamicChartType
              {...this.props}
            />
          </div>
        </div>
      </div>

    )
  }
}

export default DashWidgetContent;
