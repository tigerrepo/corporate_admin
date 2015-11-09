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
    video_url = forms.CharField(max_length=128)

    def __init__(self, *args, **kwargs):
        super(CompanyCreateForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class']='mws-textinput'
        self.fields['name'].widget.attrs['placeholder'] = 'Please input the company name'
        self.fields['slogan'].widget.attrs['placeholder'] = 'Please input the company slogan'
        self.fields['url'].widget.attrs['placeholder'] = 'URL will be http://www.riceglobal.com/corporate/ntuc if you enter ntuc here'
        self.fields['pdf_url'].widget.attrs['placeholder'] = 'Please upload introductoin pdf file'
        self.fields['video_url'].widget.attrs['placeholder'] = 'Please input the youtube video url of the company'
        self.fields['description'].widget.attrs['placeholder'] = 'Please input the company description'

    def clean_url(self):
        return self.cleaned_data['url'].lower()

    class Meta:
        model = models.Company
        fields = ['name', 'slogan', 'url', 'description', 'pdf_url', 'is_index']

class CompanyUpdateForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(CompanyUpdateForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class']='mws-textinput'

    def clean_url(self):
        return self.cleaned_data['url'].lower()

    class Meta:
        model = models.Company
        fields = ['name', 'slogan', 'url', 'description', 'is_index']


class CategoryCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryCreateForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class']='mws-textinput'

    class Meta:
        model = models.Tag
        fields = ['name', 'status']

class ProductCreateForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super(ProductCreateForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class']='mws-textinput'

    class Meta:
        model = models.Product
        fields = ['company', 'name', 'description']

class GalleryUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GalleryUploadForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class']='mws-textinput'

    class Meta:
        model = models.Gallery
        fields = ['image_url', 'name', 'is_cover']


    def on_duplicate_error(self):
        self.errors['name'] = ErrorList(['Image Name is duplicated with existing images'])
