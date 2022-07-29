from .base_views import BaseDatasourceViewSet
from blocklight_api.serializers import quickbooks_serializers
from blocklight_api.serializers.core_serializers import ChartDataSerializer

from dashboards.models import (
    Integrations_Quickbooks_Account_Info,
    Integrations_Quickbooks_Bills,
    Integrations_Quickbooks_Company_Info,
    Integrations_Quickbooks_Ledger_Reports,
    Integrations_Quickbooks_Ledger_Expenses,
    Integrations_Quickbooks_Bill_Line_Items
)


class QuickbooksAccountViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Quickbooks_Account_Info.objects.all()
    serializer_class = quickbooks_serializers.QuickbooksAccountSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'create_time'


class QuickbooksCompanyViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Quickbooks_Company_Info.objects.all()
    serializer_class = quickbooks_serializers.QuickbooksCompanySerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'create_time'


class QuickbooksBillViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Quickbooks_Bills.objects.all()
    serializer_class = quickbooks_serializers.QuickbooksBillSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'create_time'


class QuickbooksBillLineItemViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Quickbooks_Bill_Line_Items.objects.all()
    serializer_class = quickbooks_serializers.QuickbooksBillLineItemSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'bill_ref__user_iden'
    since_until_field = 'bill_ref__create_time'


class QuickbooksLedgerReportViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Quickbooks_Ledger_Reports.objects.all()
    serializer_class = quickbooks_serializers.QuickbooksLedgerReportSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'create_time'


class QuickbooksLedgerExpenseViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Quickbooks_Ledger_Expenses.objects.all()
    serializer_class = quickbooks_serializers.QuickbooksLedgerExpenseSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'ledger_ref__user_iden'
    since_until_field = 'ledger_ref__create_time'