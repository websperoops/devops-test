from .models import Widget, Dashboard, Report, BasicAuthRecords, Feedback, UserProfile 
from allauth.socialaccount.models import SocialAccount

from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
import django.forms as forms


# Custom change password form (that will show placeholders)
class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        #exclude = ('updated', 'created')

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'placeholder': 'Old password'})
        self.fields['new_password1'].widget.attrs.update({'placeholder': 'New password'})
        self.fields['new_password2'].widget.attrs.update({'placeholder': 'New password (confirm)'})

class WidgetForm(forms.ModelForm):
    class Meta:
        model = Widget
        fields = ['title', 'element', 'report']
    # def __init__(self, *args, **kwargs):
    # user = kwargs.pop('user', User.objects.get(pk_of_default_user))
    def __init__(self, user, *args, **kwargs):
        super(WidgetForm, self).__init__(*args, **kwargs)                     
        self.fields['report'] = forms.ModelChoiceField(
            queryset=SocialAccount.objects.filter(user=user))
        self.fields['report'].label_from_instance = lambda obj: "%s" % (obj.provider)

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'transaction_id' ,'integration']
    # def __init__(self, *args, **kwargs):
    # user = kwargs.pop('user', User.objects.get(pk_of_default_user))
    def __init__(self, user, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
#        initial = kwargs.pop('initial', {'integrations': kwargs['id']})
        self.fields['integration'] = forms.ModelChoiceField(
            queryset=SocialAccount.objects.filter(user=user))
        self.fields['integration'].label_from_instance = lambda obj: "%s" % (obj.provider)


class ShipStationConnectForm(forms.ModelForm):
    api_key = forms.CharField(max_length=50)
    api_secret = forms.CharField(max_length=50)
    user_iden = forms.CharField(max_length=50)
    integration_name = forms.CharField(max_length=50)
    #
    class Meta:
        model = BasicAuthRecords
        fields = ['api_key', 'api_secret', 'user_iden', 'integration_name']

class AddCustomDashboard(forms.ModelForm):
    title = forms.CharField(max_length=200)
    #
    class Meta:
        model = Dashboard
        fields = ['title']

class ReAddDeletedDashboard(forms.ModelForm):
    slug = forms.CharField(max_length=200)
    #
    class Meta:
        model = Dashboard
        fields = ['slug']

class FeedbackForm(forms.ModelForm):

    topic = forms.CharField(max_length=50, required = True)
    description = forms.CharField(max_length=500, required = True)
    
    class Meta:
        model = Feedback
        fields = ['topic', 'description']

#class ChartFeedback(forms.ModelForm):

    #topic = chart ID 

class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone_number = forms.CharField(max_length=30)
    email_address = forms.EmailField(max_length=50)
    location = forms.CharField(max_length=50)
    business_name = forms.CharField(max_length=50)
    business_website = forms.CharField(max_length=60)
    business_details = forms.CharField(max_length=500)
    industry_type = forms.CharField(max_length=30)
    product_type = forms.CharField(max_length=30)
    employee_count = forms.CharField(max_length=30)
    sales_interest = forms.BooleanField(initial=False)
    finance_interest = forms.BooleanField(initial=False)
    marketing_interest = forms.BooleanField(initial=False)
    social_interest = forms.BooleanField(initial=False)
    other_interest = forms.BooleanField(initial=False)
    other_description = forms.CharField(max_length=50)

    class Meta:
        model = UserProfile
        fields = [  'first_name', 'last_name', \
                    'phone_number', 'email_address',\
                    'business_name', 'business_website', 'business_details', \
                    'industry_type', 'product_type', 'employee_count', \
                    'sales_interest', 'finance_interest', 'marketing_interest', 'social_interest', 'other_interest', 'other_description']

class ShopifySignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First name')
    last_name = forms.CharField(max_length=30, label='Last name')
    password = forms.CharField(max_length=30, required=False)
    confirm_password = forms.CharField(max_length=30, required=False)
    accept_tos = forms.BooleanField(required=True, initial=False)
    loyalty_code = forms.CharField(max_length=30, required=False)