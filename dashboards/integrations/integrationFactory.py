from . import shipstationIntegration
from .etsy import EtsyIntegration
from .facebook_instagram.facebook import FacebookIntegration
from .facebook_instagram.instagram import InstagramIntegration
from .google import GoogleIntegration
from .mailchimp import MailchimpIntegration
from .quickbooks import QuickbooksIntegration
from .shopify import ShopifyIntegration
from .twitter import TwitterIntegration


class IntegrationFactory:

    def __init__(self):
        self._integrations = {}

    def register_integration(self, integration_name, integration):
        self._integrations[integration_name] = integration

    def get_integration(self, integration_name):
        integration = self._integrations.get(integration_name)
        if not integration:
            raise ValueError(integration_name)
        return integration


factory = IntegrationFactory()
factory.register_integration('facebook', FacebookIntegration())
factory.register_integration('google', GoogleIntegration())
factory.register_integration('instagram', InstagramIntegration())
factory.register_integration('mailchimp', MailchimpIntegration())
factory.register_integration('quickbooks', QuickbooksIntegration())
factory.register_integration('shipstation', shipstationIntegration.ShipstationIntegration())
factory.register_integration('shopify', ShopifyIntegration())
factory.register_integration('twitter', TwitterIntegration())
factory.register_integration('etsy', EtsyIntegration())
