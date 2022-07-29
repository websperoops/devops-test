from dashboards.integrations.facebook_instagram.utils import FbIgHandler


class InstagramHandler(FbIgHandler):

    def __init__(self, data, integration_id, user_iden, name, account_name):

        super(InstagramHandler, self).__init__(data, integration_id, user_iden, "instagram", name, account_name)


    def _Handler__save_independent_objects(self):
        return

    def _Handler__save_dependent_objects(self):
        return

    def _Handler__parse_data(self):
        return
