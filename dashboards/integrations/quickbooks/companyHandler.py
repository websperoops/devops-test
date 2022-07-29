from . import quickbooksHandler
from dashboards.models import Integrations_Quickbooks_Company_Info
import logging


class CompanyHandler(quickbooksHandler.QuickbooksHandler):

    logger = logging.getLogger(__name__)

    def __init__(self, data, integration_id, user_iden, integration_name, name):
        self.companys = []

        super(CompanyHandler, self).__init__(data, integration_id, user_iden, integration_name, name)
    
    def _Handler__save_independent_objects(self):
        self.save_companys()

    def _Handler__save_dependent_objects(self):
        return

    def _Handler__parse_data(self):
        company = Integrations_Quickbooks_Company_Info(
            integration_name = self.name,
            integration_id = self.integration_id,
            user_iden=self.user_iden,
            company_name=self.data.get('CompanyInfo', {}).get('CompanyName', None),
            company_address=self.data.get('CompanyInfo', {}).get('CompanyAddr', None),
            create_time = self.data.get('MetaData', {}).get('CreateTime', "2015-07-06")
        )
        self.companys.append(company)

    
    def save_companys(self):
        for company in self.companys:
            self.update_or_save_instance(Integrations_Quickbooks_Company_Info, company, "company_name")