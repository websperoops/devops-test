import axios from "axios";
import { get as _get } from "lodash";
import _ from "underscore";
import Cookies from "js-cookie";
import { data } from "jquery";

async function getPaginatedData(url) {
  let page = 0;
  let res;
  let data = [];
  do {
    page += 1;
    res = await axios.get(url, { params: { page } });
    data = data.concat(res.data.results);
  } while (res.data.next != null);
  return data;
}

function handleError(error) {
  console.error(error);
  return new Promise((r, reject) =>
    reject(_get(error, "response.data", error))
  );
}

export function getChartTypeId(name) {
  return axios
    .get(`/api/v1/chart_types/?name=${name}`)
    .then((data) => data.data, handleError);
}

export function getUserProfile() {
  return axios
    .get("/api/v1/user_profiles/")
    .then((data) => data.data, handleError);
}

export function updateUserInfo(data, id) {
  return axios
    .patch(`/api/v1/users/${id}/`, data, {
      headers: { "X-CSRFTOKEN": Cookies.get("csrftoken") },
    })
    .then((data) => data.data, handleError);
}

export function updateUserProfile(data, id) {
  return axios
    .patch(`/api/v1/user_profiles/${id}/`, data, {
      headers: { "X-CSRFTOKEN": Cookies.get("csrftoken") },
    })
    .then((data) => data.data, handleError);
}

export function getUserInfo() {
  return axios.get("/api/v1/users/").then((data) => data.data, handleError);
}

export function getDashboardsList() {
  return getPaginatedData("/api/v1/dashboards").catch((err) =>
    handleError(err)
  );
}

export function getIntegrationsList() {
  return getPaginatedData("/api/v1/integrations").catch((err) =>
    handleError(err)
  );
}

export function getInsightsList() {
  return axios.get("/api/v1/timeline_insights").then(data => data.data, handleError)
}

export function getPredefinedMetrics(integrationsNames) {
  return getPaginatedData(
    `/api/v1/predefined_metrics/?predefined_integrations__name__inall=${integrationsNames.join()}&predefined_dashboard__isnull=True`
  ).catch((err) => handleError(err));
}

export function getPredefinedMetricTypes(predefinedMetricId) {
  return getPaginatedData(
    `/api/v1/predefined_metric_types/?predefined_metric=${predefinedMetricId}`
  ).catch((err) => handleError(err));
}

export function getPredefinedChartTypes(predefinedMetricId) {
  return getPaginatedData(
    `/api/v1/predefined_chart_types/?predefined_metric=${predefinedMetricId}`
  ).catch((err) => handleError(err));
}

export function getPredefinedTimeRanges(predefinedMetricId) {
  return getPaginatedData(
    `/api/v1/predefined_time_ranges/?predefined_metric=${predefinedMetricId}`
  ).catch((err) => handleError(err));
}

export function getFavoriteDashboard() {
  return axios
    .get(`/api/v1/dashboards/`, { params: { is_favorite: true } })
    .then(
      // Every User should have one favorite dashboard (created during signup)
      (data) => data.data.results[0],
      handleError
    );
}

export function getDashboard(dashboardId) {
  return axios
    .get(`/api/v1/dashboards/${dashboardId}/`)
    .then((data) => data.data, handleError);
}

export function addDashboard(dashboardObj) {
  return axios
    .post(`/api/v1/dashboards/`, dashboardObj, {
      headers: { "X-CSRFTOKEN": Cookies.get("csrftoken") },
    })
    .then((data) => data.data, handleError);
}

export async function renameDashboard(name, dashId) {
  return axios
    .patch(
      `/api/v1/dashboards/${dashId}/`,
      { name },
      { headers: { "X-CSRFTOKEN": Cookies.get("csrftoken") } }
    )
    .then((data) => data.data, handleError);
}

export async function deleteDashboard(dashId) {
  return axios
    .delete(`/api/v1/dashboards/${dashId}/`, {
      headers: { "X-CSRFTOKEN": Cookies.get("csrftoken") },
    })
    .then((data) => data.data, handleError);
}

export function getDashboardLayoutList(dashboardId) {
  return getPaginatedData(
    `/api/v1/dashboards_layouts/?dashboard_id=${dashboardId}`
  ).catch((err) => handleError(err));
}

export function updateDashboardLayout(dashboardLayoutId, data) {
  return axios
    .put(`/api/v1/dashboards_layouts/${dashboardLayoutId}/`, data, {
      headers: { "X-CSRFTOKEN": Cookies.get("csrftoken") },
    })
    .then((data) => data.data, handleError);
}

export function getChart(chartId) {
  return axios
    .get(`/api/v1/charts/${chartId}/`)
    .then((data) => data.data, handleError);
}

export function editMetric(chartData, metricId) {
  return axios
    .patch(`/api/v1/metrics/${metricId}/`, chartData.metric, {
      headers: { "X-CSRFTOKEN": Cookies.get("csrftoken") },
    })
    .then((data) => data.data, handleError);
}

export function editTimeRange(id, data) {
  return axios
    .patch(`/api/v1/time_ranges/${id}/`, data, {
      headers: { "X-CSRFTOKEN": Cookies.get("csrftoken") },
    })
    .then((data) => data.data, handleError);
}

export function addChart(chartData) {
  return axios
    .post(`/api/v1/charts/add_chart/`, chartData, {
      headers: { "X-CSRFTOKEN": Cookies.get("csrftoken") },
    })
    .then((data) => data.data, handleError);
}

export function deleteChart(chartId) {
  return axios
    .delete(`/api/v1/charts/${chartId}/`, {
      headers: { "X-CSRFTOKEN": Cookies.get("csrftoken") },
    })
    .then((data) => data.data, handleError);
}

function _paramsTransferUnderscoreToHyphensInKeys(params) {
  return _.pairs(params)
    .map(
      (paramKeyVal) => paramKeyVal[0].replace("_", "-") + "=" + paramKeyVal[1]
    )
    .join("&");
}

export function getDataSourceObj(url) {
  return axios
    .get(`/api/v1/data_sources/?url=${encodeURIComponent(url)}`)
    .then((data) => data.data)
    .catch((err) => handleError(err));
}

export function sendAbandonedCartEmail(data) {
  return axios
    .post("/dashboards/send_abandoned_cart_email/", data, {
      headers: { "X-CSRFTOKEN": Cookies.get("csrftoken") },
    })
    .then((data) => data.data, handleError);
}

export function getSocialAccounts() {
  return axios
    .get("/api/v1/social_accounts/")
    .then((data) => data.data)
    .catch((err) => handleError(err));
}

// time range for social post
export function getSocialTimeRange() {
  return axios
    .get("/api/v1/topsocial_timeranges/")
    .then((data) => data.data.results)
    .catch((err) => handleError(err));
}

// top facebook post
export function getFacebookPostsTotalEngagements(since) {
  return axios
    .get(
      `/api/v1/facebook_page_posts/chart_data/?filter=()&timerange-since=${since}&timerange-until=now&group-by=month_dynamic,permalink,post_id,permalink&aggregate=integrations_facebook_page_post_engagements__value__sum`
    )
    .then((data) => (data.data.results ? data.data.results : []))
    .catch((err) => handleError(err));
}

export function getFacebookPostsTotalReactions(since) {
  return axios
    .get(
      `/api/v1/facebook_page_posts/chart_data/?filter=()&timerange-since=${since}&timerange-until=now&group-by=month_dynamic,permalink,post_id,permalink&aggregate=integrations_facebook_page_post_reactions__value__sum`
    )
    .then((data) => (data.data.results ? data.data.results : []))
    .catch((err) => handleError(err));
}

export function getFacebookPost(postId) {
  return axios
    .get(`/api/v1/facebook_page_posts/?filter=post_id__eq=${postId}`)
    .then((data) => (data.data.results.length ? data.data.results[0] : null))
    .catch((err) => handleError(err));
}

export function getFacebookPostImpressions(postId) {
  return axios
    .get(
      `/api/v1/facebook_page_posts/chart_data/?filter=(post_id=${postId})&group-by=permalink,post_id,permalink,integrations_facebook_page_post_impressions__name&aggregate=integrations_facebook_page_post_impressions__value__sum`
    )
    .then((data) => (data.data.results.length ? data.data.results : null))
    .catch((err) => handleError(err));
}

export function getFacebookPostReactions(postId) {
  return axios
    .get(
      `/api/v1/facebook_page_posts/chart_data/?filter=(post_id=${postId})&group-by=permalink,post_id,permalink,integrations_facebook_page_post_reactions__name&aggregate=integrations_facebook_page_post_reactions__value__sum`
    )
    .then((data) => (data.data.results.length ? data.data.results : null))
    .catch((err) => handleError(err));
}

// top instagram post
export function getInstagramPostsTotalEngagements(since) {
  return axios
    .get(
      `/api/v1/instagram_media_objects/chart_data/?filter=(is_story=False)&timerange-since=${since}&timerange-until=now&group-by=month_dynamic,permalink,media_id,is_story,timestamp&aggregate=integrations_instagram_media_insights_engagements__value__sum`
    )
    .then((data) =>
      data.data.results
        ? data.data.results.filter((result) => result.media_id !== null)
        : []
    )
    .catch((err) => handleError(err));
}

export function getInstagramPost(postId) {
  return axios
    .get(`/api/v1/instagram_media_objects/?filter=media_id=${postId}`)
    .then((data) => (data.data.results.length ? data.data.results[0] : null))
    .catch((err) => handleError(err));
}

export function getInstagramImpressions(postId) {
  return axios
    .get(
      `/api/v1/instagram_media_objects/chart_data/?filter=(media_id=${postId})&group-by=permalink,media_id,timestamp&aggregate=integrations_instagram_media_insights_impressions__value__sum`
    )
    .then((data) => (data.data.results.length ? data.data.results[0] : null))
    .catch((err) => handleError(err));
}

//Timeline calls

export async function getPaginatedTimelineData(page) {
  try {
    const res = await axios
      .get("/api/v1/business_timeline/", { params: { page } })
      .catch((err) => handleError(err));
    return res.data.results;
  } catch (error) {
    handleError(error)
  }
}

export function getChartData(datasource, params) {
  const paramsStr = _paramsTransferUnderscoreToHyphensInKeys(params);
  return getPaginatedData(`/api/v1${datasource}?${paramsStr}`).catch((err) =>
    handleError(err)
  );
}

export function getChartDataTimeRange(
  datasource,
  group_by,
  aggregate,
  since,
  until,
  dynamic,
  filter,
  insight
) {
  insight = (typeof insight !== 'undefined') ?  insight : ""
  return getPaginatedData(
    `/api/v1${datasource}?filter=(${filter})&timerange-since=${since}&timerange-until=${until}&group-by=${dynamic}_dynamic,${group_by}&aggregate=${aggregate}${insight}`
  ).catch((err) => handleError(err));
}

export async function getTimelinePageData (
  datasource,
  group_by,
  aggregate,
  since,
  until,
  dynamic,
  filter,
  insight,
  page
) {
  insight = (typeof insight !== 'undefined') ?  insight : ""
  page = (typeof page !== 'undefined') ? page : ""
  const url = `/api/v1${datasource}?filter=(${filter})&timerange-since=${since}&timerange-until=${until}&group-by=${dynamic}_dynamic,${group_by}&aggregate=${aggregate}${insight}`
  try {
    const res = await axios
      .get(url, { params: { page } })
      .catch((err) => handleError(err));
    return res.data.results;
  } catch (error) {
    handleError(error)
  }


}

export function getDataSourceList() {
  return getPaginatedData("/api/v1/data_sources/").catch((err) =>
    handleError(err)
  );
}

export function getSummaryIntegrationsList() {
  return getPaginatedData("/api/v1/summary_integrations").catch((err) =>
    handleError(err)
  );
}

export function getSummaryMetricData() {
  return axios
    .get("/api/v1/summary_metrics")
    .then((data) => data.data, handleError);
}

export function getSummaryTimeRange() {
  return axios
    .get("/api/v1/summary_time_ranges/")
    .then((data) => data.data.results, handleError);
}

export function getActiveSub() {
  return axios
    .get("/api/v1/active_subscription/")
    .then((data) => data.data, handleError);
}
