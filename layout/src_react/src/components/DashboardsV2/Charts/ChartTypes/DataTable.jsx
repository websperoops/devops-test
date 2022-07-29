import React, { Component } from 'react';
import { DataGrid, GridToolbar } from '@material-ui/data-grid';
import { AutoSizer } from 'react-virtualized';
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';

const theme = createMuiTheme({
  palette: {
      primary: { main: '#ef7c15' }
  },
});

class Table extends Component {
    constructor(props) {
        super(props);
        this.state = {
            columns: [],
            data: [],
        }

        this.headingMapping = {
            'campaign_id': 'Campaign ID',
            'date_created': 'Date Created',
            'status': 'Status',
            'archive_url': 'Archive URL',
            'campaign_creation_time': 'Time to Create',
            'send_time': 'Sent',
            'from_name': 'From',
            'title': 'title',
            'subject_line': 'Subject Line',
            'emails_sent__sum': 'Emails Sent',
            'opens__sum': 'Opens',
            'unique_opens__sum': 'Unique Opens',
            'open_rate__sum': 'Open Rate (%)',
            'clicks__sum': 'Clicks',
            'subscriber_clicks__sum': 'Subscriber Clicks',
            'click_rate__sum': 'Click Rate (%)',
            'total_orders__sum': 'Total Orders',
            'total_revenue__sum': 'Total Revenue ($)',
            'total_spent__sum': 'Total Spent ($)',
            'campaign_aov__sum': 'AOV ($)',
            'campaign_id': 'Campaign ID',
            'open_rate__min': 'Open Rate (%)',
            'click_rate__min': 'Click Rate (%)',
            'total_spent__min': 'Total Spent ($)'
        }
    }

    componentDidMount() {
        Object.keys(this.props.chartData[0]).forEach((obj) => {
            this.setState((prev) => ({ columns: [...prev.columns, { name: this.headingMapping[obj], selector: obj, sortable: true }] }))
    })


        this.props.chartData.forEach(item => {
            const value = {}
            Object.keys(item).forEach(i => {
                if (!isNaN(Number(item[i]))) {
                    value[i] = Number(item[i]).toFixed(2)
                    if (i.includes('rate')) {
                        value[i] = Number((value[i] * 100).toFixed(0))
                    }
                }
                else {
                    value[i] = item[i]
                }
            })
            this.setState((prev) => ({ data: [...prev.data, value] }))
        })
    }

    render() {

        const rows = this.props.chartData.map((item, index) => {
            const out = {'id': index}
            Object.keys(item).forEach(i => {
                out[i] = isNaN(item[i]) ? item[i] : (Number(item[i]) % 1 === 0 ? Number(item[i]) : Number(item[i]).toFixed(2)) // maybe try to check if percentage or something
            })
            return out
        })
        const columnData = Object.keys(this.props.chartData[0])

        return (
            <AutoSizer>
                {({ height, width }) => {
                    const pageSize = Math.floor(11*(height)/rows.length/12);
                    const columns = columnData.map(item => {
                        return {field: item, headerName: this.headingMapping[item], width: 9*width/columnData.length/10} // add column type
                    })
                    return (
                        <div style={{ height: `${height + 30}px`, width: `${width}px`, overflowY: 'auto' }}>
                            <MuiThemeProvider theme={theme}>
                                <DataGrid
                                    hideToolbar={false}
                                    autoHeight
                                    pageSize={pageSize}
                                    rows={rows}
                                    columns={columns}
                                    components={{
                                        Toolbar: GridToolbar
                                    }}
                                    className={'orange_text'}
                                />
                            </MuiThemeProvider>
                        </div>
                    );
                }}
            </AutoSizer>
        );
    }
}

export default Table;