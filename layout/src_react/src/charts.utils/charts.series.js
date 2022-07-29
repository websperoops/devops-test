function getTooltipHeader(interval) {
    if (interval == 'hours') {
        var new_xDateFormat = '%H:%M %b %d, %Y';
        var new_headerFormat = '<span style="font-size:12px; padding-bottom:4px;"><b>Hour of: {point.key}</b></span><table>';
    } else if (interval == 'days') {
        var new_xDateFormat = '%b %d, %Y';
        var new_headerFormat = '<span style="font-size:12px; padding-bottom:4px;"><b>Day of: {point.key}</b></span><table>';
    } else if (interval == 'weeks') {
        var new_xDateFormat = '%b %d, %Y';
        var new_headerFormat = '<span style="font-size:12px; padding-bottom:4px;"><b>Week of: {point.key}</b></span><table>';
    } else if (interval == 'months') {
        var new_xDateFormat = '%b %Y';
        var new_headerFormat = '<span style="font-size:12px; padding-bottom:4px;"><b>Month of: {point.key}</b></span><table>';
    }
    return [new_xDateFormat, new_headerFormat];
}

function getTooltipPoint(data_label) {
    if (data_label == '$') {
        var new_pointFormat = '<tr><td style="color:{series.color}; padding-right:2px;"><b>{series.name}: </b></td>' +
            '<td style="padding:0"><b>${point.y:.2f}</b></td></tr>';
    } else if (data_label == '%') {
        var new_pointFormat = '<tr><td style="color:{series.color}; padding-right:2px;"><b>{series.name}: </b></td>' +
            '<td style="padding:0"><b>{point.y:.2f}%</b></td></tr>';
    } else {
        var new_pointFormat = '<tr><td style="color:{series.color}; padding-right:2px;"><b>{series.name}: </b></td>' +
            '<td style="padding:0"><b>{point.y} ' + data_label + '</b></td></tr>';
    }
    return new_pointFormat;
}

function getTooltipMap(data_label) {
    if (data_label == '$') {
        var new_pointFormat = '<tr><td style="color:{series.color}; padding-right:2px;"><b>{point.full}: </b></td>' +
            '<td style="padding:0"><b>${point.value:.2f}</b></td></tr>';
    } else if (data_label == '%') {
        var new_pointFormat = '<tr><td style="color:{series.color}; padding-right:2px;"><b>{point.full}: </b></td>' +
            '<td style="padding:0"><b>{point.value:.2f}%</b></td></tr>';
    } else {
        var new_pointFormat = '<tr><td style="color:{series.color}; padding-right:2px;"><b>{point.full}: </b></td>' +
            '<td style="padding:0"><b>{point.value} ' + data_label + '</b></td></tr>';
    }
    return ['', new_pointFormat];
}
//create series

export const pieSeries = (chart, data) => {
    chart.addSeries({ data: [] })
    let points = [];
    // for (var i = 0; i < data.series.length; i++) {
    //     chart.series[0].addPoint({ name: data.series[i].name, y: data.series[i].data });
    //     console.log([data.series[i].name, data.series[i].data])
    //     console.log(i)
    //     if (data.data_label == '$') { var data_format = '<b>{point.name}</b>:<br>${point.y}'; } else if (data.data_label == '%') { var data_format = '<b>{point.name}</b>:<br> {point.y}' + data.data_label; } else { var data_format = '<b>{point.name}</b>:<br> {point.y} ' + data.data_label; }
    //     chart.series[0].points[i].update({ dataLabels: { format: data_format } });

    //     console.log(chart.series[0].points[i])
    // }

    if (data.data_label == '$') { var data_format = '<b>{point.name}</b>:<br>${point.y}'; } else if (data.data_label == '%') { var data_format = '<b>{point.name}</b>:<br> {point.y}' + data.data_label; } else { var data_format = '<b>{point.name}</b>:<br> {point.y} ' + data.data_label; }
    data.series.map((s, i) => {
        points.push([s.name, s.data])
        if (points.length == data.series.length) {
            chart.series[0].setData(points)
                // chart.series[0].points.map(point => point.update({ dataLabels: { format: data_format } }))
        }
    })

    chart.redraw()


}

export const dualAxisSeries = (chart, data) => {
    while (chart.yAxis.length > 0) {
        chart.yAxis[0].remove();
    }
    for (var i = 0; i < data.series.length; i++) {
        // First need to convert dates (xAxis) to real Date objects
        for (var j = 0; j < data.series[i].data.length; j++) {
            data.series[i].data[j][0] = Date.parse(data.series[i].data[j][0])
        }
        chart.addAxis({
            title: {
                text: data.series[i].yAxis_title,
                style: { color: '#ffffff' }
            },
            labels: {
                format: '{value}',

            },
            opposite: Boolean(i % 2 == 0)
        });
        chart.addSeries({
            name: data.series[i].name,
            type: data.series[i].type,
            yAxis: data.series[i].yAxis,
            data: data.series[i].data
        }, false);
        // Add $ or % to yAxis labels if necessary
        if (data.data_label[i] == '$') {
            chart.yAxis[i].update({
                labels: {
                    formatter: function() { return '$' + this.axis.defaultLabelFormatter.call(this); }
                }
            });
        } else if (data.data_label[i] == '%') {
            chart.yAxis[i].update({
                labels: {
                    formatter: function() { return this.axis.defaultLabelFormatter.call(this) + '%'; }
                }
            });
        }
        // Otherwise make sure yAxis labels are normal
        else {
            chart.yAxis[i].update({
                labels: {
                    formatter: function() { return this.axis.defaultLabelFormatter.call(this); }
                }
            });
        }
        // Change date/time format
        var new_headerFormat = getTooltipHeader(data.interval);
        chart.series[i].update({ tooltip: { xDateFormat: new_headerFormat[0], headerFormat: new_headerFormat[1] } });
        // Change data format
        var new_pointFormat = getTooltipPoint(data.data_label[i]);
        chart.series[i].update({ tooltip: { pointFormat: new_pointFormat } });

    }

    chart.redraw()

}

export const chartSeries = (chart, data, type = null) => {
    if (data.data_label == '$') {
        chart.yAxis[0].update({
            labels: {
                formatter: function() {
                    console.log('$' + this.axis.defaultLabelFormatter.call(this), 'axis', data, chart.yAxis[0])
                    return '$' + this.axis.defaultLabelFormatter.call(this);
                }
            }
        });
    } else if (data.data_label == '%') {
        chart.yAxis[0].update({
            labels: {
                formatter: function() {
                    console.log(this.axis.defaultLabelFormatter.call(this) + '%', 'axis', data, chart.yAxis[0])

                    return this.axis.defaultLabelFormatter.call(this) + '%';
                }
            }
        });
    }

    // If stacked column, update stack total format
    if (type == 'Stacked_Column') {
        if (data.data_label == '$') { var total_format = '<b>Total</b>:<br> ${total}'; } else { var total_format = '<b>Total</b>:<br> {total} ' + data.data_label; }
        chart.yAxis[0].update({ stackLabels: { format: total_format } });
    }
    for (var i = 0; i < data.series.length; i++) {
        // First need to convert dates (xAxis) to real Date objects
        for (var j = 0; j < data.series[i].data.length; j++) {
            data.series[i].data[j][0] = Date.parse(data.series[i].data[j][0])
        }
        // Add series
        chart.addSeries({ name: data.series[i].name, data: data.series[i].data }, false);
        // Change date/time format
        var new_headerFormat = getTooltipHeader(data.interval);
        chart.series[i].update({ tooltip: { xDateFormat: new_headerFormat[0], headerFormat: new_headerFormat[1] } });
        // Change data format
        var new_pointFormat = getTooltipPoint(data.data_label);
        chart.series[i].update({ tooltip: { pointFormat: new_pointFormat } });
    }
    chart.redraw();
}

export const USA_MapSeries = (chart, data) => {
    var correct_series = []
    for (var i = 0; i < data.series.length; i++) {
        if ('code' in data.series[i]) {
            correct_series.push(data.series[i]);
        }
    }
    // Add series
    chart.addSeries({
        animation: { duration: 1000 },
        data: correct_series,
        joinBy: ['hc-key', 'code'],
        name: data.data_label,
        dataLabels: {
            enabled: true,
            color: '#FFFFFF',
            format: '{point.abbrev}'
        }
    }, false);
    // Change tooltip format
    var new_Format = getTooltipMap(data.data_label);
    chart.series[0].update({ tooltip: { headerFormat: new_Format[0], pointFormat: new_Format[1] } });
    // Redraw
    chart.redraw();

}