////////////DashboardWidget////////////////////////////////////
import React, { useContext, createContext, useState, useEffect, usePrevious, useReducer } from 'react';
import { ReducerContext } from '../../index';
import Reducer from '../../reducer/reducer'
import { PieTheme, AreaTheme, DualAxisTheme, StackedColumnTheme, LineTheme, ColumnTheme } from '../../charts.utils/charts.themes';
import { pieOptions, areaOptions, dualAxisOptions, stackedColumnOptions, lineOptions, columnOptions } from '../../charts.utils/charts.options';
import { pieSeries, chartSeries, dualAxisSeries } from '../../charts.utils/charts.series';
import { Chart, Single_Metric } from '../Charts/Charts';










// Dash Menu









