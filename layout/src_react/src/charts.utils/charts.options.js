//Chart Options 
import { PieTheme, DualAxisTheme, StackedColumnTheme, AreaTheme, ColumnTheme, LineTheme } from './charts.themes'

export const pieOptions = (data, id) => {
    if (data.data_label == '$') { var data_format = '<b>{point.name}</b>:<br>${point.y}'; } else if (data.data_label == '%') { var data_format = '<b>{point.name}</b>:<br> {point.y}' + data.data_label; } else { var data_format = '<b>{point.name}</b>:<br> {point.y} ' + data.data_label; }

    return {

        ...PieTheme,
        // maintainAspectRatio: false,
        // options: {
        //     maintainAspectRatio: false,
        // },
        credits: {
            enabled: false
        },
        id: id,
        // plotOptions: {
        //     pie: {
        //       allowPointSelect: true,
        //       dataLabels: {
        //         crop: false,
        //         distance: 25,
        //         overflow: "none",
        //         style: {
        //           fontSize: "10px",
        //           width: "60px"
        //         }
        //       },
        //     }
        //   },
        responsive: {
            rules: [{
                condition: {
                    // maxWidth: 500,
                    maxHeight: 190
                },
                chartOptions: {
                    chart: {
                        //     x: 40,
                        //   height: 290,
                        //   spacing: [2, 2, 2, 2]
                    },
                    title: {
                        //   y: 55
                    },
                    subtitle: {
                        // text: null
                        // x: 15
                    },
                    title: {
                        text: null
                    },
                    plotOptions: {

                        pie: {
                            dataLabels: {
                                enabled: false,
                            },

                        }
                    }
                }
            }]
        },
        chart: {
            type: 'pie',
            // paddingLeft: 5,
            // height: 250,
            // width: 300,
            // plotBackgroundColor: null,
            // plotBorderWidth: null,
            // plotShadow: false,
            // options3d: {
            //     enabled: false,
            //     alpha: 45
            // },
            marginBottom: 20 //so labels dont get cut off when theres lots of them
        },
        // lang: {
        //     thousandsSep: ','
        // },
        // title: {
        //     // text: data.title,
        //     text: null,
        //     style: {
        //         color: '#000000',
        //         fontWeight: 'bold',
        //     }
        // },
        subtitle: {
            text: data.subtitle,
        },
        tooltip: {
            pointFormat: '{point.percentage:.1f} %'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    format: data_format
                }

            },
        },
        xAxis: {
            visible: false
        },
        yAxis: {
            visible: false
        }
        // series: []

    };
}



export const dualAxisOptions = (data, id) => {

    //     if (data.data_label == '$') {
    //     chart.yAxis[0].update({
    //         labels: {
    //             formatter: function() { return '$' + this.axis.defaultLabelFormatter.call(this); }
    //         }
    //     });
    // } else if (data.data_label == '%') {
    //     chart.yAxis[0].update({
    //         labels: {
    //             formatter: function() { return this.axis.defaultLabelFormatter.call(this) + '%'; }
    //         }
    //     });
    // }
    // // Otherwise make sure yAxis labels are normal
    // else {
    //     chart.yAxis[0].update({
    //         labels: {
    //             formatter: function() { return this.axis.defaultLabelFormatter.call(this); }
    //         }
    //     });
    // }


    return {
        ...DualAxisTheme,
        credits: {
            enabled: false
        },
        id,
        chart: {
            zoomType: 'xy',
            spacingBottom: 25
        },
        title: {
            text: data.title
        },
        subtitle: {
            text: data.subtitle
        },
        xAxis: [{ crosshair: true, type: 'datetime', visible: true }, ],
        yAxis: [{
            title: {
                style: {
                    color: '#000000',
                },
                visible: true
            }

        }, { //secondary axis
            title: {
                style: {
                    color: '#000000',
                },
            }

        }],
        tooltip: {
            headerFormat: '<span style="font-size:12px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y}</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            x: 80,
            verticalAlign: 'top',
            y: 55,
            floating: true,
            backgroundColor: 'rgba(255,255,255,0.8)'
        },
        series: [],
    }
}

export const stackedColumnOptions = (data, id) => ({
    ...StackedColumnTheme,
    credits: {
        enabled: false
    },
    id: id,
    chart: {
        type: 'column',
        spacingBottom: 25

    },
    colors: ['#e98535', '#dd403a', '#456990', '#dfd6a7', '#36413e', '#698996', '#c17c74', '#247BA0', '#bcac9b', '#ffe0b5'],
    title: {
        // text: 'Stacked column chart' (set via JS)
        text: data.title
    },
    subtitle: {
        // text: 'Stacked column chart' (set via JS)
        text: data.subtitle
    },
    xAxis: {
        // categories: ['Apples', 'Oranges', 'Pears', 'Grapes', 'Bananas'] (set via JS - not anymore)
        title: {
            // text: 'Total fruit consumption' (set via JS)
            text: data.xAxis_title,
            style: {
                color: '#ffffff'
            },
            visible: true,
        },
        type: 'datetime'
    },
    yAxis: {
        visible: true,
        min: 0,
        title: {
            // text: 'Total fruit consumption' (set via JS)
            text: data.yAxis_title,
            style: {
                color: '#ffffff'
            }
        },
        stackLabels: {
            enabled: true,
            style: {
                fontWeight: 'bold',
                color: 'white',
            },
            y: -25
        }
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        x: -30,
        verticalAlign: 'top',
        y: 25,
        floating: true,
        backgroundColor: 'rgba(255,255,255,0.8)',
        borderColor: '#CCC',
        borderWidth: 1,
        shadow: false
    },
    tooltip: {
        headerFormat: '<span style="font-size:12px">{point.key}</span><table>',
        pointFormat: '<tr> <td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y}</b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true
    },
    plotOptions: {
        column: {
            stacking: 'normal',
            dataLabels: {
                enabled: false, // Turn this back on to display labels all the time
                color: 'white'
            }
        }
    },
    series: []
});

export const areaOptions = (data, id) => {

    return {
        ...AreaTheme,
        credits: {
            enabled: false
        },
        id: id,
        chart: {
            type: 'area',
            spacingBottom: 10

        },
        colors: ['#eb8527', '#FFCA3D', '#babbbd', '#2e86ab', '#d20c0f'],
        title: {
            align: "left",
            text: data.title,
        },
        subtitle: {
            text: data.subtitle
        },
        xAxis: {
            visible: true,
            title: {
                text: data.xAxis_title,
                style: {
                    color: '#ffffff'
                }
            },
            type: 'datetime'
        },
        yAxis: {
            visible: true,
            title: {
                text: data.yAxis_title,
                style: {
                    color: '#ffffff'
                }
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y}</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            area: {
                marker: {
                    enabled: false,
                    symbol: 'circle',
                    radius: 2,
                    states: {
                        hover: {
                            enabled: true
                        }
                    }
                }
            }
        },

        series: [],
        responsive: {
            rules: [{
                condition: {
                    // maxWidth: 500
                },
            }]
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            x: 80,
            verticalAlign: 'top',
            y: 50,
            floating: true,
            backgroundColor: 'rgba(255,255,255,0.8)'
        },


    }
}

export const columnOptions = (data, id) => ({
    ...ColumnTheme,
    credits: {
        enabled: false
    },
    id: id,
    chart: {
        type: 'column',
        marginBottom: 10
    },
    colors: ['#e98535', '#dd403a', '#456990', '#dfd6a7', '#36413e', '#698996', '#c17c74', '#247BA0', '#bcac9b', '#ffe0b5'],
    title: {
        // text: 'Stacked column chart' (set via JS)
        text: data.title
    },
    subtitle: {
        // text: 'Stacked column chart' (set via JS)
        text: data.subtitle
    },
    xAxis: {
        visible: true,
        // categories: ['Apples', 'Oranges', 'Pears', 'Grapes', 'Bananas'] (set via JS - not anymore)
        title: {
            // text: 'Total fruit consumption' (set via JS)
            text: data.xAxis_title,
            style: {
                color: '#ffffff'
            }
        },
        type: 'datetime'
    },
    yAxis: {
        visible: true,
        min: 0,
        title: {
            // text: 'Total fruit consumption' (set via JS)
            text: data.yAxis_title,
            style: {
                color: '#ffffff'
            }
        },
        stackLabels: {
            enabled: true,
            style: {
                fontWeight: 'bold',
                color: 'white',
            },
            y: -25
        }
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        x: -30,
        verticalAlign: 'top',
        y: 25,
        floating: true,
        backgroundColor: 'rgba(255,255,255,0.8)',
        borderColor: '#CCC',
        borderWidth: 1,
        shadow: false
    },
    tooltip: {
        headerFormat: '<span style="font-size:12px">{point.key}</span><table>',
        pointFormat: '<tr> <td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y}</b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true
    },
    plotOptions: {
        column: {
            stacking: 'normal',
            dataLabels: {
                enabled: false, // Turn this back on to display labels all the time
                color: 'white'
            }
        }
    },
    series: []
})

export const lineOptions = (data, id) => ({
    ...LineTheme,
    credits: {
        enabled: false
    },
    chart: {
        type: 'line',
        spacingBottom: 25

    },
    id: id,
    title: {
        // text: 'Solar Employment Growth by Sector, 2010-2016' (set via JS)
    },
    subtitle: {
        // text: 'Source: thesolarfoundation.com' (set via JS)
        text: data.subtitle
    },
    xAxis: {
        visible: true,
        title: {
            text: data.xAxis_title,
            // text: 'Year' (set via JS)
            style: {
                color: '#000000'
            }
        },
        type: 'datetime'
    },
    yAxis: {
        visible: true,
        title: {
            // text: 'Number of Employees' (set via JS)
            text: data.yAxis_title,
            style: {
                color: '#000000'
            }
        }
    },
    tooltip: {
        headerFormat: '<span style="font-size:12px">{point.key}</span><table>',
        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y}</b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle',
        backgroundColor: 'rgba(255,255,255,0.8)'
    },
    plotOptions: {
        series: {
            label: {
                connectorAllowed: false
            }
        }
    },
    series: [],
    responsive: {
        rules: [{
            condition: {
                // maxWidth: 500
            },
            chartOptions: {
                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'bottom'
                }
            }
        }]
    }

})

export const USA_MapOptions = (data, id) => {

    return {
        credits: {
            enabled: false
        },
        chart: {
            map: 'countries/us/us-all',
            borderWidth: 0
        },
        id: id,
        title: {
            // text: 'US population density (/km²)' (set via JS)
        },
        subtitle: {
            // text: 'Source: thesolarfoundation.com' (set via JS)
            text: data.subtitle
        },
        exporting: {
            enabled: false
        },

        legend: {
            layout: 'vertical',
            borderWidth: 0,
            backgroundColor: "none",
            //floating: true,
            align: 'left',
            verticalAlign: 'bottom'
                //y: 25
        },

        mapNavigation: {
            enabled: true,
            buttonOptions: {
                align: 'right',
                verticalAlign: 'bottom'
            },
        },

        colorAxis: {
            min: 1,
            type: 'linear',
            minColor: '#fffe55',
            maxColor: '#d20c0f',
            stops: [
                [0, '#ffffff'],
                [0.01, '#fffe55'],
                [0.67, '#eb8527'],
                [1, '#d20c0f']
            ]
        },

        series: []
    }
}