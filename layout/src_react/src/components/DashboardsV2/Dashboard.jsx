import React, { Component } from 'react';
import _ from 'underscore';
import { WidthProvider, Responsive } from 'react-grid-layout';
const ResponsiveReactGridLayout = WidthProvider(Responsive);

import DashboardHeader from './DashboardHeader';

import {
  getDashboard,
  getDashboardsList,
  getDashboardLayoutList,
  updateDashboardLayout,
  getChart,
  getChartData,
  saveChartLayout,
  getUserProfile,
  updateUserProfile,
  getSocialAccounts
} from '../../api/BLApi';
import DashWidget from './DashWidget';
import { chart } from 'highcharts';

class Dashboard extends Component {
  constructor(props) {
    super(props);
    this.GrlRef = React.createRef();

    this.state = {
      dashboard: {},
      dashboardsList: [],
      charts: {},
      chartsData: {},
      user:{},
      // gridCols: {lg: 48, md: 36, sm: 24, xs: 12, xxs: 12},  // responsive
      gridCols: 48, // not responsive
      gridColsCount: 48, // used to calculate width of chart // TOTO: can read actual value in reponsive mode?
      gridWidth: 1200,
      gridRowHeight: 50,
      gridLayoutObj: [],
      chartIdsLayoutIds: {},
      isHomepage: false,
      isSyncing: false
    };
    this._handleLayoutChange = this._handleLayoutChange.bind(this);
    this._saveGridLayoutObj = this._saveGridLayoutObj.bind(this);
    this._loadDashboardChartsData = this._loadDashboardChartsData.bind(this);
    this.loadChartData = this.loadChartData.bind(this);
    this._loadDashboardList = this._loadDashboardList.bind(this);
    this._setChartData = this._setChartData.bind(this);
    this.removeChartFromGridLayout = this.removeChartFromGridLayout.bind(this);
    this._getNewChartLayout = this._getNewChartLayout.bind(this);
  }

  componentDidMount() {
    getUserProfile().then(data => {
			this.setState({
				user: data.results[0]
			})
			let res=data.results[0]
			let id=res.id
			if(!res.has_visited_dashboard && res.has_integrated_social_account){
				updateUserProfile({has_visited_dashboard : true}, id).then(data=>{
				})
			
			}
		})
    this.setState({
      isHomepage: window.location.href.includes('homepage'),
    });
    this._loadDashboardList();
    this._loadDashboardChartsData();

    getSocialAccounts().then(data=>{
      let account;
      for(let i=0; i<data.results.length; i++){
        if(data.results[i].id === this.state.dashboard.account){
          account = data.results[i]
          break
        }
      }

      this.setState({
        isSyncing: JSON.parse(account.extra_data.replace(/'/g,'"').toLowerCase().replace(/none/g,'"None"')).syncing
      })
    })
  }

  _loadDashboardList() {
    getDashboardsList().then((dashboardsList) =>
      this.setState({
        dashboardsList: dashboardsList,
      })
    );
  }

  _loadDashboardChartsData(charts) {
    getDashboard(this.props.dashboardId).then((dashboard) => {
      this.setState({
        dashboard: dashboard,
      });

      getDashboardLayoutList(this.props.dashboardId).then((layoutData) => {
        let ld = Object.fromEntries(
          layoutData.map((obj) => [
            obj['chart_id'],
            {
              w: obj['w'],
              h: obj['h'],
              x: obj['x'],
              y: obj['y'],
              minW: 2,
              maxW: undefined,
              minH: 4,
              maxH: undefined,
              moved: false,
              static: this.GrlRef.current.state.width > 768 ? false : true,
              isDraggable: undefined,
              isResizable: undefined,
            },
          ])
        );

        let cl = Object.fromEntries(
          layoutData.map((obj) => [obj['chart_id'], obj['id']])
        );

        this.setState({
          gridLayoutObj: ld,
          chartIdsLayoutIds: cl,
        });
      });

      this.loadChartData(charts);
    });
  }

  _setChartData(chart, id) {
    this.setState((state, props) => ({
      charts: {
        ...state.charts,
        [id]: chart,
      },
    }));

    const chartDataParams = {
      filter: chart.metric.filter,
      group_by: chart.metric.time_group_by
        ? `${chart.metric.time_group_by},${chart.metric.group_by}`
        : chart.metric.group_by,
      aggregate: chart.metric.aggregate,
      ...(chart.metric.time_range && {
        timerange_since: chart.metric.time_range.since,
        timerange_until: chart.metric.time_range.until,
      }),
    };

    getChartData(chart.metric.datasource, chartDataParams).then((chartsData) =>
    {
      this.setState((state, props) => ({
        chartsData: {
          ...state.chartsData,
          [id]: chartsData,
        },
      }))
    }
    );
  }

  loadChartData(charts = this.state.dashboard.charts) {
    charts.map((chartId) => {
      getChart(chartId).then((chart) => this._setChartData(chart, chartId));
    });
  }

  removeChartFromGridLayout(chartId) {
    this.setState({
      gridLayoutObj: _.omit(this.state.gridLayoutObj, chartId),
    });
  }

  _saveGridLayoutObj(layout) {
    // from list oj objects create object with keys
    //		from 'i'-s in array's objects
    let layoutObj = Object.fromEntries(
      layout.map((obj) => [obj['i'], _.omit(obj, 'i')])
    );
    // TODO: Update only changed dashboards_layouts data
    _.intersection(
      Object.keys(layoutObj),
      Object.keys(this.state.chartIdsLayoutIds)
    ).map((chartId) => {
      updateDashboardLayout(this.state.chartIdsLayoutIds[chartId], {
        id: this.state.chartIdsLayoutIds[chartId],
        x: layoutObj[chartId]['x'],
        y: layoutObj[chartId]['y'],
        w: layoutObj[chartId]['w'],
        h: layoutObj[chartId]['h'],
        dashboard_id: Number(this.props.dashboardId),
        chart_id: Number(chartId),
      }).then((r) => {
        this.setState((state, props) => ({
          gridLayoutObj: {
            ...state.gridLayoutObj,
            // NOTE: Note from where the chatId Is. It's not the function parameter
            [chartId]: layoutObj[chartId],
          },
        }));
      });
    });
  }

  _handleLayoutChange(layout) {
    if (this.GrlRef.current.state.width > 768) {
      //if breakpoint is bigger than mobile save layout if moved around or resized
      this._saveGridLayoutObj(layout);
    }
  }

  _getNewChartLayout() {
    return {
      x: 0,
      y:
        Object.values(this.state.gridLayoutObj).length > 0
          ? Math.max(
              ...Object.values(this.state.gridLayoutObj).map((l) => l.y)
            ) + 1
          : 0,
      w: 20,
      h: 5,
    };
  }

  render() {
    return (
      <>
        {this.state.dashboardsList[0] && !this.state.isHomepage && this.state.dashboard.name && (
          <DashboardHeader
            dashboardId={this.props.dashboardId}
            dashName={this.state.dashboard.name}
            getNewChartLayoutFunc={this._getNewChartLayout}
            reloadDashboardFunc={this._loadDashboardChartsData}
            dashboardsList={this.state.dashboardsList}
            _loadDashboardList={this._loadDashboardList}
            defaultDashboard={this.state.dashboardsList[0]}
            reloadDashboardFunc={this._loadDashboardChartsData}
          />
        )}

        {
          this.state.isSyncing ? 
          <div style={{'paddingLeft':'12px','fontSize':'18px'}}>This dashboard is unavailable while we sync your data. Please check back soon.</div> 
          : 
          (<ResponsiveReactGridLayout
            className='layout mb-4'
            rowHeight={this.state.gridRowHeight}
            // onLayoutChange={this._handleLayoutChange} // saves layout too many times while resizing or dragging.
            onResizeStop={this._handleLayoutChange}
            onDragStop={this._handleLayoutChange}
            margin={[15, 15]}
            preventCollision={false}
            breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
            cols={{ lg: 12, md: 12, sm: 12, xs: 3, xxs: 1 }}
            layouts={{ lg: [] }} // do not remove. will cause layout to mess up whe switching from xs to lg
            measureBeforeMount={true}
            ref={this.GrlRef}
            compactType={
              this.GrlRef.current && this.GrlRef.current.state.width > 768
                ? 'vertical'
                : 'horizontal'
            }
            draggableHandle='.menu'
          >
            {Object.keys(this.state.chartsData).length > 0 ? (
              Object.keys(this.state.chartsData).map((chartId) =>
                // react-grid-stack has a dependency to have a div with 'key' here.
                // 	  It's not working on div inside DashWidget or
                // 	  at the DashWidget itself
                Object.keys(this.state.gridLayoutObj).includes(chartId) ? (
                  <div
                    key={chartId}
                    data-grid={this.state.gridLayoutObj[chartId]}
                  >           
                    <DashWidget
                      key={chartId}
                      datagrid={this.state.gridLayoutObj[chartId]}
                      chartId={chartId}
                      chartName={this.state.charts[chartId].metric.name}
                      title={this.state.charts[chartId].metric.title}
                      xFieldName={this.state.charts[chartId].metric.x_field}
                      xAxisTitle={this.state.charts[chartId].metric.x_label}
                      yFieldName={this.state.charts[chartId].metric.y_field}
                      yAxisTitle={this.state.charts[chartId].metric.y_label}
                      groupFieldName={
                        this.state.charts[chartId].metric.group_field
                      }
                      groupName={this.state.charts[chartId].metric.group_label}
                      chartType={
                        this.state.charts[chartId].metric.chart_type.name
                      }
                      chartData={this.state.chartsData[chartId]}
                      metricId={this.state.charts[chartId].metric.id}
                      premetricId={
                        this.state.charts[chartId].predefined_metric.id
                      }
                      loadChartData={this.loadChartData}
                      integrations_id={
                        this.state.charts[chartId].metric.integrations
                      }
                      time_range_id={
                        this.state.charts[chartId].metric.time_range
                          ? this.state.charts[chartId].metric.time_range.id
                          : null
                      }
                      // time_range_id={this.state.charts[chartId].metric.time_range.id}
                      removeChartFromGridLayoutFunc={
                        this.removeChartFromGridLayout
                      }
                      getNewChartLayoutFunc={this._getNewChartLayout}
                    />
                  </div>
                ) : (
                  <div />
                )
              )
            ) : (
              <div />
            )}
          </ResponsiveReactGridLayout>)
        }
      </>
    );
  }
}
export default Dashboard;