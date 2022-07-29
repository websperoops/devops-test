from dashboards.models import (
    Integrations_Quickbooks_Account_Info,
    Integrations_Quickbooks_Bills,
    Integrations_Quickbooks_Company_Info,
    Integrations_Quickbooks_Ledger_Reports,
    Integrations_Quickbooks_Ledger_Expenses,
    Integrations_Quickbooks_Bill_Line_Items
)

from rest_framework import serializers


class QuickbooksAccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Quickbooks_Account_Info
        fields = [
            'user_iden',
            'account_id',
            'name',
            'current_balance',
            'active',
            'create_time',
            'last_update_time'
        ]


class QuickbooksCompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Quickbooks_Company_Info
        fields = [
            'user_iden',
            'company_name',
            'company_address',
            'create_time'
        ]


class QuickbooksBillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Quickbooks_Bills
        fields = [
            'user_iden',
            'due_date',
            'balance',
            'bill_id',
            'create_time',
            'last_update_time'
        ]


class QuickbooksBillLineItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Quickbooks_Bill_Line_Items
        fields = [
            'user_iden',
            'item_id',
            'item_name',
            'description',
            'amount',
            'unit_price',
            'detail_type',
            'quantity',
        ]


class QuickbooksLedgerReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Quickbooks_Ledger_Reports
        fields = [
            'user_iden',
            'account_id',
            'account_name',
            'beginning_balance',
            'ending_balance',
            'transaction_balance',
            'start_period',
            'end_period',
            'create_time'
        ]


class QuickbooksLedgerExpenseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Quickbooks_Ledger_Expenses
        fields = [
            'user_iden',
            'transaction_id',
            'date',
            'category',
            'transaction_type',
            'vendor',
            'description',
            'amount',
            'current_ledger_value'
        ]