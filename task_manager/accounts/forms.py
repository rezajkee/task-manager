from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from .utils import PlaceholderMixin


class UserRegistrationForm(PlaceholderMixin, forms.ModelForm):
    label_1 = _('PasswordTitle')
    label_2 = _('PasswordConfirm')
    help_text1 = _('PasswordHelpText')
    help_text2 = _('PasswordConfirmHelpText')
    password = forms.CharField(label=label_1, help_text=help_text1, widget=forms.PasswordInput)
    password2 = forms.CharField(label=label_2, help_text=help_text2, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            output = _('PasswordMismatch')
            raise forms.ValidationError(output)
        return cd['password2']