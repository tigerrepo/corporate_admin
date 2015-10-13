from django import forms
from tiger_admin import models
from django.forms.util import ErrorList

class AccountPasswordResetForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password_confirm = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(AccountPasswordResetForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class']='mws-textinput'

    def on_password_differnt_error(self):
        self.errors['new_password'] = ErrorList(['Confirm password is not the same as new password'])
        self.errors['new_password_confirm'] = ErrorList(['Confirm password is not the same as new password'])

    def on_password_incorrect(self):
        self.errors['old_password'] = ErrorList(['Old password is not correct'])

    class Meta:
        model = models.Account
        fields = []


class CompanyCreateForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)
    tag = forms.ModelChoiceField(queryset=models.Tag.objects.all())
    def __init__(self, *args, **kwargs):
        super(CompanyCreateForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class']='mws-textinput'

    def clean_url(self):
        return self.cleaned_data['url'].lower()

    class Meta:
        model = models.Company
        fields = ['name', 'slogan', 'url', 'description']

class CategoryCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryCreateForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class']='mws-textinput'

    class Meta:
        model = models.Tag
        fields = ['name']
