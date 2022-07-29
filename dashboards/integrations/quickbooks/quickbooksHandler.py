from dashboards.integrations.utils import Handler
import logging


class QuickbooksHandler(Handler):

    logger = logging.getLogger(__name__)

    def __init__(self, data, integration_id, user_iden, integration_name, name):

        '''
        This class is meant to be inherited to sync shopify objects/resources from the
        python shopify API wrapper library.


        Args:
            data (dict): API response data from the shopify wrapper library.
            integration_id (int): the id for the integraion
            user_iden (int): the user's id
            shop_id (int): the associated shops id
            name (str): hardcoded name specifying the core object/resource
        '''
        super(QuickbooksHandler, self).__init__(data, integration_id, user_iden, "quickbooks", name)

    def __save_independent_objects(self):
        return
    
    def __save_dependent_objects(self):
        return
    
    def __parse_data(self):
        return

