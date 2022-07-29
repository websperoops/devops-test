import React, { useReducer, useState, useEffect, useLayoutEffect, Suspense } from 'react'
import { PieTheme, AreaTheme, DualAxisTheme, StackedColumnTheme, LineTheme, ColumnTheme, USA_MapTheme } from '../../charts.utils/charts.themes';
import { pieOptions, areaOptions, dualAxisOptions, stackedColumnOptions, lineOptions, columnOptions, USA_MapOptions } from '../../charts.utils/charts.options';
import { pieSeries, chartSeries, dualAxisSeries, USA_MapSeries } from '../../charts.utils/charts.series';
import { ReducerContext } from '../../index';
import Reducer from '../../reducer/reducer'
import DashWidget from './DashWidget';
import { addInitialWidgets, getData, getPath } from '../../functions/dashboard/dashFunctions'

function DashWidgetGrid() {
    const [data, setData] = useState();
    const [state, dispatch] = useReducer(Reducer, {
        charts: [],
        chartPaths: [],
        chartUpdate: null,
        chartFavorite: null,
        chartDelete: null,
        chartAdd: null,
        chartsJson: [],
        chartDetails: [
            { type: 'pie', theme: PieTheme, options: pieOptions, createSeries: pieSeries },
            { type: 'area', theme: AreaTheme, options: areaOptions, createSeries: chartSeries },
            { type: 'dual_axis', theme: DualAxisTheme, options: dualAxisOptions, createSeries: dualAxisSeries },
            { type: 'stacked_column', theme: StackedColumnTheme, options: stackedColumnOptions, createSeries: chartSeries },
            { type: 'line', theme: LineTheme, options: lineOptions, createSeries: chartSeries },
            { type: 'column', theme: ColumnTheme, options: columnOptions, createSeries: chartSeries },
            { type: 'usa_map', theme: USA_MapTheme, options: USA_MapOptions, createSeries: USA_MapSeries }
        ],
    });


    useEffect(() => {
        let charts = widget_charts && widget_charts.map(chart => {
            chart.path = getPath(chart)
            chart.json = getData(chart)
            return chart;


        }) //add path and json to object
        console.log(charts)

        dispatch({ type: 'initialLoad', payload: charts })

    }, [widget_charts])



    useLayoutEffect(() => {
        addInitialWidgets(state.charts);

    }, [state.charts])






    const [modal, setModal] = useState(null);
    const [modals] = useState([
        { name: 'DeleteChart', action: 'Delete', path: '/dashboards/remove_chart/?slug=' },
        { name: 'FaveChart', action: 'Favorite', path: '/dashboards/add_chart_to_favorites/?chart_id=' }
    ])
    const [selectedChartId, setSelectedChartId] = useState(null);

    const toggleModal = (type, id) => {
        switch (type) {
            case 'DeleteChart':
                setModal('DeleteChart');
                setSelectedChartId(id);
                break;

            case 'FaveChart':
                setModal('FaveChart');
                setSelectedChartId(id);
                break;

            default:
                setModal(null)
                setSelectedChartId(null)
                break;
        }
    }

    const showCharts = () => {
        if ($('#grid')) $('#grid').addClass('grid-stack')
        if ($('#favorites_dash')) $('#favorites_dash').addClass('grid-stack');

        return (
            <div className="grid-stack h-100">
                <ReducerContext.Provider value={{ state, dispatch }}>
                    {state.charts && state.charts.map((chart, chartIndex) => {
                        return (<DashWidget chart={chart}
                            toggleModal={toggleModal}
                            key={chartIndex}
                            id={chart.id}
                            title={chart.metric}
                            type={chart.current_chart_type} />
                        )
                    })

                    }

                </ReducerContext.Provider>

            </div>
        )
    }

    const showNoCharts = () => {
        var isFave;
        if (dashboards) {
            isFave = dashboards.filter(dash => dash.tab_index === '0')[0].id == parseInt(window.location.href.split('/')[4])
        }
        else {
            isFave = true;
        }

        if ((window.location.href.indexOf("/dashboards/homepage/") > -1) || isFave) {
            return (
                <div className="text-center">
                    <h3>You haven't favorited any charts!</h3>
                </div>
            )
        }
        else if (window.location.href.indexOf("view") > -1 && !isFave) {
            return (<div className="text-center d-flex flex-column justify-content-center align-items-center">
                <h3>You Don't have any charts! Start By taking the following action:</h3>
                <a className=" text-light pt-1 btn_orange btn_long" href="../../integrations">Add An Integration</a>
            </div>)
        }
    }

    return (
        <>

            {state.charts.length ? showCharts() : showNoCharts()}
        </>
    )
};

export default DashWidgetGrid;