from dashboards.integrations.utils import Handler
import datetime
import logging


class TwitterHandler(Handler):

    logger = logging.getLogger(__name__)

    def __init__(self, data, integration_id, user_iden, integration_name, name):

        super(TwitterHandler, self).__init__(data, integration_id, user_iden, integration_name, name)

    def __save_independent_objects(self):
        return

    def __save_dependent_objects(self):
        return

    def __parse_data(self):
        return

    def getTimeStamp(self, datetimeString):
        ''' RETURNS datetime object based on date/time format from twitter API'''
        if not datetimeString:
            return None

        month_mapping = {
            'Jan': 1,
            'Feb': 2,
            'Mar': 3,
            'Apr': 4,
            'May': 5,
            'Jun': 6,
            'Jul': 7,
            'Aug': 8,
            'Sep': 9,
            'Oct': 10,
            'Nov': 11,
            'Dec': 12
        }
        date = datetimeString.split(" ")
        year, month, day = int(date[-1]), month_mapping[date[1]], int(date[2])
        clocktime = date[3].split(":")
        hour, minute, second = int(clocktime[0]), int(
            clocktime[1]), int(clocktime[2])
        timestamp = datetime.datetime(year, month, day, hour, minute, second)
        return timestamp

