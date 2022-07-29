from . import googleHandler
from datetime import datetime
from django.db import transaction
from django.utils import timezone
import pytz


class MetricsHandler(googleHandler.GoogleHandler):

    def __init__(self, data, integration_id, user_iden, model,profile):

        self.report_rows = []
        self.model = model
        self.profile = profile
        super(MetricsHandler, self).__init__(data, integration_id, user_iden, str(model.__class__.__name__))


    def _Handler__save_independent_objects(self):
        with transaction.atomic():
            self.save_report_rows()


    def _Handler__save_dependent_objects(self):
        with transaction.atomic():
            pass


    def _Handler__parse_data(self):
        columnHeader = self.data.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
        self.data = self.data.get("data", {}).get("rows",[])

        for obj in self.data:
            r = {}
            dims = obj.get("dimensions", [])
            for i in range(len(dims)):
                r[dimensionHeaders[i]] = dims[i]

            metrics = obj.get("metrics", [])[0]
            values = metrics.get("values", [])
            for i in range(len(values)):
                r[metricHeaders[i]["name"]] = values[i]

            self.report_rows.append(r)


    def save_report_rows(self):
        if self.model.objects.filter(profile=self.profile).count() < 1:
            date = timezone.datetime(year=2004, month=1, day=1)  # earliest possible date in google analytics
            latest = pytz.timezone('UTC').localize(date)
        else:
            latest = self.model.objects.filter(profile=self.profile).latest('datehour').datehour
        create = []
        user_iden = self.profile.web_property.account.social_account.user_id
        last_sync_time = timezone.now()

        for data in self.report_rows:
            # figure out if needs update or created
            datehour = pytz.timezone(self.profile.time_zone).localize(datetime.strptime(data["ga:dateHour"], "%Y%m%d%H"))
            if datehour <= latest:  # need an upate
                self.model.sync(self.profile, data)
            else:  # can put into list for bulk create
                create.append(self.model.create_obj(data, self.profile, user_iden, datehour, last_sync_time))
        self.model.objects.bulk_create(create)
