import Highcharts from 'highcharts';
import gridstack from 'gridstack'
import 'gridstack/dist/gridstack.jQueryUI';
import 'gridstack/dist/jquery-ui'
import lodash from 'lodash'
import $ from 'jquery';


export const getData = async(chart) => {
    let path = getPath(chart)
    if (path.indexOf('google') > -1) {

        path = path.replace('Past_1_Day', 'Past_Day')
    }
    if (path.indexOf('#') > -1) {
        path = path.replace(/#/g, '%23')
    }
    const res = await fetch(path.replace(/#/g, '%23'));
    const json = await res.json();
    return json
};



export function getPath(chart) {
    var option;
    if (chart.current_option === null) {
        option = '{}';
    } else if (chart.current_option.value) {
        option = `{%27value%27:%27${chart.current_option.value}%27}`
    }


    var path = chart_data_url +
        "?chart_id=" + chart.id +
        "&integration=" + chart.integration +
        "&metric=" + chart.metric +
        "&option=" + option +
        "&chart_type=" + chart.current_chart_type +
        "&time_period=" + chart.current_time_period +
        "&dashboard_id=" + chart.dashboard +
        "&what_changed=" + "current_chart_type"

    return path;

}


export function addInitialWidgets(charts) {



    // Make grid and position chart containers
    var options = {
        resizable: { handles: 'se, ,sw,' },
        animate: true,
        cellHeight: 70,
        verticalMargin: 10,
        float: false,
        draggable: {
            handle: '.menu',
            scroll: true,
            appendTo: '.grid-stack',
        }
    };

    $('.grid-stack').gridstack(options);

    var maxHeight = '';
    var minWidth = '';
    var maxWidth = '';
    var minHeight = '';
    var chart_x, chart_y, chart_height, chart_width;

    var grid = $('#grid').data('gridstack') || $('#favorites_dash').data('gridstack');

    charts.map((chart, index) => {
        var chart_id = chart.id.split("_").slice(0, -1).join('_'); // DO NOT CHANGE

        if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
            console.log(chart)
            $(".graph").children(".menu").css("visibility", "unset")
            chart_x = "0";
            chart_y = "0";
            chart_width = "12";
            chart_height = "5";

        } else if (window.location.pathname == '/dashboards/homepage/') {
            chart_x = 0;
            chart_y = 0;
            chart_width = '3'
            chart_height = '3'

            grid.compact();


        } else {
            chart_x = chart.positions[0]
            chart_y = chart.positions[1]
            chart_width = chart.positions[2]
            chart_height = chart.positions[3]

        };
        if (chart.current_chart_type === 'Single_Metric') {
            minWidth = 3;
            minHeight = 3
            maxWidth = 6;
            maxHeight = 5;
        } else {
            minWidth = 3;
            minHeight = 3;
            maxWidth = 12;
            maxHeight = 12;
        }

        if (window.location.href.indexOf('view') > -1) {
            // isFavoriteSlug = dashboards.filter(dash => dash.tab_index == '0')[0].id === parseInt(window.location.href.split('/')[4])
        }
        grid.addWidget(document.getElementById(chart.id + "_container"), chart_x, chart_y, chart_width, chart_height, false, minWidth, 12, (minHeight || 3), maxHeight, chart.id);
        $('.shield').css('visibility', 'hidden');



        // Hide chart shield, resize chart when chart drag stops
        // $(`.grid-stack`).on('gsresizestop', function(event, elem) {
        //     $('.shield').css('visibility', 'hidden')
        //     var chart_id = chart.id.split("_").slice(0, -1).join('_'); // DO NOT CHANGE
        //     console.log(chart.id)

        // });


        window.addEventListener('resize', function() {
            resizeHighchart(chart.id)
        })



        // Save changed widget locations anytime grid changes
        $('.grid-stack').on('change', function(event, items) {
            if (typeof items !== 'undefined') {
                saveGrid(items, chart)
            }
        });

        //only resize the chart when its parent window is being resized
        $(`#${chart.id}_container`).on('resize', function(e, ui) {
            resizeHighchart(chart.id)
        })

        $(`#${chart.id}_container`).bind("resizestop", function(event, ui) {
            console.log(ui)
            setTimeout(resizeHighchart(chart.id, ui.size.height, ui.size.width), 800) //give it time to get correct dimensions

        });

        // Resize all charts when window changes size
        // $(window).on('resize', function() {
        //     resizeHighchart(chart.id)

        // })


    })
};

export const resizeHighchart = (id, height, width) => {
    const chartIndex = Highcharts.charts.findIndex(chart => chart.userOptions.id == id)
    const currentChart = Highcharts.charts[chartIndex]
    var $outerBox = $(document.getElementById(id + "_container"));

    if (currentChart) {
        console.log(currentChart.userOptions.id)
        currentChart.update({
            chart: {
                height: height * 0.65 || $outerBox.height() * 0.65,
                width: width * 0.90 || $outerBox.width() * 0.90,
            },
            title: {
                text: '', //get rid of the title 
                align: 'center'

            },
        });
        currentChart.reflow();
    }
}

export function saveGrid(items, chart) {
    // Build dict (string) with all chart locations
    let chart_positions = "{";
    items.map(item => {
        chart_positions += "'" + item.el["0"].id.split("_").slice(0, -1).join('_') + "' : {" +
            "'x_position' : " + item.x + ", " +
            "'y_position' : " + item.y + ", " +
            "'width' : " + item.width + ", " +
            "'height' : " + item.height + "},";
    })
    chart_positions = chart_positions.slice(0, -1) + "}";
    // Call function to save chart locations in DB
    if (chart.widget_header && window.location.href.indexOf('view') > -1) { //only save position if in dashboards page
        var path = save_chart_url +
            "?dashboard_id=" + parseInt(window.location.href.split('/')[4]) + //temporary until we can pass tab_id from django
            "&chart_positions=" + chart_positions;

        $.getJSON(path);

    }


}


export function newResizeChart(chart_id) {
    // Resize non-chart divs
    var $outerBox = $(document.getElementById(chart_id + "_0_container"));

    // Resize table (if DataTable)
    try {
        var table = document.getElementById(chart_id + "_iframe").contentDocument.getElementById("datatable");
        var height = ($outerBox.height() * 0.85).toString() + "px";
        var width = ($outerBox.width() * 0.85).toString() + "px";
        table.setAttribute("style", "height: " + height + ", width: " + width);
    } catch (err) {

    }
}



export const csrf_token = getCookie('csrftoken');

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export async function requestNewChartOptions(id) {
    var path = `${new_chart_options_url}?dashboard_id=${id}`;
    const res = await fetch(path);
    return await res.json();
}


export function dataTableLoad(chart_id, data) {
    var initialized = document.getElementById(chart_id + "_iframe").contentWindow.checkInitialized();
    if (!initialized) {

        // Get table title and subtitle tags, then set
        //chart.title.update({text: ''});
        // = data.title
        var title = document.getElementById(chart_id + "_iframe").contentDocument.getElementById("title");
        var subtitle = document.getElementById(chart_id + "_iframe").contentDocument.getElementById("subtitle");
        document.getElementById(chart_id + "_menu").children[0].innerHTML = data.title

        subtitle.innerHTML = data.subtitle;

        // Get table column names and data divs in iframe, then clear
        var names_div = document.getElementById(chart_id + "_iframe").contentDocument.getElementById("names");
        var data_div = document.getElementById(chart_id + "_iframe").contentDocument.getElementById("data");
        names_div.innerHTML = "";
        data_div.innerHTML = "";

        // Fill column names
        names_div.insertAdjacentHTML('beforeend', "<th>#</th>  \n");
        for (var i = 0; i < data.columns.length; i++) {
            names_div.insertAdjacentHTML('beforeend', "<th>" + data.columns[i] + "</th>  \n");
        }

        // Fill data
        for (var i = 0; i < data.series.length; i++) {
            // Build html for row
            if (i % 2 == 0) {
                var row = "<tr class='odd'> \n";
            } else {
                var row = "<tr class='even'> \n";
            }
            row += "<td>" + (i + 1).toString() + "</td> \n";
            for (var j = 0; j < data.columns.length; j++) {
                row += "<td>" + data.series[i][data.columns[j]] + "</td> \n";
            }
            row += "</tr> \n";
            // Insert
            data_div.insertAdjacentHTML('beforeend', row);
        }

        // Initialize
        document.getElementById(chart_id + "_iframe").contentWindow.initializeTable();
    }

    // Else just edit titles and add data to existing table
    else {

        // Get table title and subtitle tags, then set
        var title = document.getElementById(chart_id + "_iframe").contentDocument.getElementById("title");
        document.getElementById(chart_id + "_menu").children[0].innerHTML = data.title
        var subtitle = document.getElementById(chart_id + "_iframe").contentDocument.getElementById("subtitle");

        subtitle.innerHTML = data.subtitle;
        // Edit data
        document.getElementById(chart_id + "_iframe").contentWindow.newData(data);
    }
}