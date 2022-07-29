// export async function loadSummaryChart(chart_id, path) {


//     if (path.indexOf('#') > -1) {
//         path = path.replace(/#/g, "%23");
//     }

//     if (path.indexOf('google') > -1) {
//         path = path.replace('Past_1_Day', "Past_Day");
//     }

//     var response = await fetch(path);
//     var data = await response.json();

//     console.log(data)
//     return data;
// }


export async function summaryLoad(chart, id) {

    let current_time_period = chart.current_time_period;
    if (chart.current_time_period === 'null') {
        current_time_period = 'All_Time';
    }

    var path = chart_data_url +
        "?chart_id=" + chart.id +
        "&integration=" + chart.integration +
        "&metric=" + chart.metric +
        "&option=" + '{}' +
        "&chart_type=" + "Single_Metric" +
        "&time_period=" + current_time_period +
        "&dashboard_id=" + chart.dashboard +
        "&what_changed=" + "initial_load";

    if (path.indexOf('#') > -1) {
        path = path.replace(/#/g, "%23");
    }

    if (path.indexOf('google') > -1) {
        path = path.replace('Past_1_Day', "Past_Day");
    }

    var response = await fetch(path);
    var data = await response.json();

    return data;
}

export async function changeSummaryTime(chart, newTime, id) {

    var path = chart_data_url +
        "?chart_id=" + chart.id +
        "&integration=" + chart.integration +
        "&metric=" + chart.metric +
        "&option=" + '{}' +
        "&chart_type=" + "Single_Metric" +
        "&time_period=" + newTime +
        "&dashboard_id=" + chart.dashboard +
        "&what_changed=" + "initial_load";


    var response = await fetch(path);
    var data = await response.json();

    return data;

}

export function changeSummaryAccount(chart, account, id) { //will add later to modal

    var path = chart_data_url +
        "?chart_id=" + chart.id +
        "&integration=" + chart.integration +
        "&metric=" + chart.metric +
        "&option=" + `{%23value%23: ${account}}` +
        "&chart_type=" + "Single_Metric" +
        "&time_period=" + chart.current_time_period +
        "&dashboard_id=" + chart.dashboard +
        "&what_changed=" + "current_option";
    loadSummaryChart(id, path);

}