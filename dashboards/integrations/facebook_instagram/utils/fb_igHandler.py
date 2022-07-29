from dashboards.integrations.utils import Handler


class FbIgHandler(Handler):

    def __init__(self, data, integration_id, user_iden, integration_name,name, account_name):

        self.insights = {}
        self.account_name = account_name
        self.value_counts = 0
        self.unique_value_counts=0
        super(FbIgHandler, self).__init__(data, integration_id, user_iden, integration_name, name)


    def _Handler__save_independent_objects(self):
        return

    def _Handler__save_dependent_objects(self):
        return

    def _Handler__parse_data(self):
        return
    
