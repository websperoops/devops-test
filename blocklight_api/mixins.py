from blocklight_api.filters import OwnerSpecificFilterBackend, ShopifySelectedStoreFilterBackend
from rest_framework.settings import api_settings


class UserSpecificFilteringMixin():
    """
    Mixin to filter queryset in the context of currently logged-in user.
    The subclass needs to provide 'owner_field_refference'(:string)
    which is used in 'queryset.filter' method to filter queryset by user_id
    E.g: owner_field_refference = 'dashboard__user'
    For dynamic building of this refference, the 'get_owner_field_refference'
    method can be overwrote.
    For special cases the 'get_owner_filter_kwargs' can be overwrote.
    """

    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS \
        + [OwnerSpecificFilterBackend]

    def __init__(self, *args, **kwargs):
        super(UserSpecificFilteringMixin, self).__init__(*args, **kwargs)
        if not (
            hasattr(self.__class__, 'owner_field_reference')
            or hasattr(self.__class__, 'get_owner_field_reference ')
            # TODO: Maybe would be nice to have, but it needs fine-tuning
            # or hasattr(self.__class__, 'get_owner_filter_kwargs')
        ):
            raise NotImplementedError(
                "Class must have field 'owner_field_refference' or"
                " overwrite get_owner_field_refference or"
                " get_owner_filter_kwargs method"
            )

    def get_owner_field_refference(self):
        return getattr(self, 'owner_field_reference', None)

    def get_owner_filter_kwargs(self, request):
        """
        Used by OwnerSpecificFilterBackend to filter querysed based on
        currently logged-in User.
        """
        return {self.get_owner_field_refference(): request.user.id}


class ShopifySelectedStoreFilteringMixin():

    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS \
        + [ShopifySelectedStoreFilterBackend]

    def __init__(self, *args, **kwargs):
        super(ShopifySelectedStoreFilteringMixin,
              self).__init__(*args, **kwargs)
