from .models import BlogSubscribe

from django import forms
from django.forms.forms import BaseForm


class BlogSubscribeForm(forms.Form):
    email = forms.CharField(label="email", max_length=100)

    class Meta:
        model = BlogSubscribe
        fields = ('email')

class AsDiv(BaseForm):

    def as_div(self):
        return self._html_output(
            normal_row = u'<div%(html_class_attr)s class="col-md-offset-4 col-md-4 col-xs-offset-2 col-xs-8" >%(errors)s%(label)s %(field)s%(help_text)s</div>',
            error_row = u'<div>%s</div>',
            row_ender = '</div>',
            help_text_html = u' <span class="helptext">%s</span>',
            errors_on_separate_row = False)

class PasswordForm(forms.Form):
    password = forms.CharField(max_length=30, required=False)
    confirm_password = forms.CharField(max_length=30, required=False)


class PasswordResetForm(forms.Form):
    email_address = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')


class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First name')
    last_name = forms.CharField(max_length=30, label='Last name')
    email_address = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    email_confirm = forms.EmailField(max_length=254, help_text ='Required.  Inform a valid email address.')
    loyalty_code = forms.CharField(max_length=30, label='Loyalty Code', required=False)
    accept_tos = forms.BooleanField(required=True, initial=False)