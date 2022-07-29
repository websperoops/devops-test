import datetime
import requests


def strp_fb_time(insight_value):
    date = insight_value.get("end_time", None)
    if date:
        date = datetime.datetime.strptime(date,  "%Y-%m-%dT%H:%M:%S+%f")
    return date


def is_insight_data_within_two_years(insight_data):
    two_yrs_ago = datetime.datetime.now() - datetime.timedelta(days=2*365)
    parse_insight_date = lambda insight_value : strp_fb_time(insight_value)
    if len(insight_data) < 1:
        return False
    for pckt in insight_data:
        insight_values = pckt.get("values",[])
        insight_dates = list(map(parse_insight_date,insight_values))
        insight_dates = list(filter((None).__ne__, insight_dates))
        oldest_found = min(insight_dates)
        newest_found = max(insight_dates)
        print("oldest_found:", oldest_found)
        print("newest_found:", newest_found)
        if two_yrs_ago > newest_found or len(insight_dates) < 1:
            return False
    return True


def is_media_object_data_within_two_years(object_data,access_token):
    two_yrs_ago = datetime.datetime.now() - datetime.timedelta(days=2*365)
    parse_object_date = lambda object : datetime.datetime.strptime(object["timestamp"],  "%Y-%m-%dT%H:%M:%S+%f")
    if len(object_data) < 1:
        return False

    first_id = object_data[0]["id"]
    last_id = object_data[-1]["id"]

    check_first_obj_date_url = "https://graph.facebook.com/v8.0/{}?fields=timestamp&access_token={}".format(first_id,access_token)
    check_last_obj_date_url = "https://graph.facebook.com/v8.0/{}?fields=timestamp&access_token={}".format(last_id,access_token)


    first_response = requests.get(check_first_obj_date_url).json()
    last_response = requests.get(check_last_obj_date_url).json()


    first_date = parse_object_date(first_response)
    last_date = parse_object_date(last_response)
    print("first_date", first_date, "last_date", last_date)
    if two_yrs_ago > first_date or two_yrs_ago > last_date:
        return False
    else:
        return True


def is_fb_post_data_within_two_years(object_data):
    two_yrs_ago = datetime.datetime.now() - datetime.timedelta(days=2*365)
    parse_object_date = lambda object : datetime.datetime.strptime(object["created_time"],  "%Y-%m-%dT%H:%M:%S+%f")
    if len(object_data) < 1:
        return False
    first_object = object_data[0]
    last_object = object_data[-1]

    first_date = parse_object_date(first_object)
    last_date = parse_object_date(last_object)

    if two_yrs_ago > first_date or two_yrs_ago > last_date:
        return False
    else:
        return True
