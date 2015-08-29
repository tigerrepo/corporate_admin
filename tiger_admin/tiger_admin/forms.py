from django import forms
from tiger_admin import models

class AccountPasswordResetForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password_confirm = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(AccountPasswordResetForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class']='mws-textinput'

    def clean(self):
        old = self.cleaned_data.get('old_password')
        new = self.cleaned_data.get('new_password')
        new_confirm = self.cleaned_data.get('new_password_confirm')
        if old and new and new_confirm:
            if new != new_confirm:
                raise forms.ValidationError('Confirm Password is not the same as new password')
            return self.cleaned_data
        else:
            raise forms.ValidationError('123213')

    class Meta:
        model = models.Account
