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
        self.fields['address'].widget.attrs['placeholder'] = 'Please input the company address'
        self.fields['tel'].widget.attrs['placeholder'] = 'Please input the company telephone'
        self.fields['email'].widget.attrs['placeholder'] = 'Please input the company email'
        self.fields['fax'].widget.attrs['placeholder'] = 'Please input the company fax'
        self.fields['pdf_url'].required = False

    def clean_url(self):
        return self.cleaned_data['url'].lower()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not "@" in email or not '.' in email:
            raise forms.ValidationError('Email is not valid')
        return email

    def clean_tel(self):
        tel = self.cleaned_data['tel']
        if not tel.isdecimal():
            raise forms.ValidationError('Telephone number must be all digits')
        return tel

    def clean_fax(self):
        fax = self.cleaned_data['fax']
        if not fax.isdecimal():
            raise forms.ValidationError('Fax number must be all digits')
        return fax

    def clean_video_url(self):
        url = str(self.cleaned_data['video_url'])
        if not url.startswith("http://") and not url.startswith("https://") and not '=' in url:
            raise forms.ValidationError('Video Url must be start with http:// or https:// and contain =')
        if '=' not in url:
            raise forms.ValidationError('Video Url must be youtube format and contain = ')
        return url

    class Meta:
        model = models.Company
        fields = ['name', 'slogan', 'url', 'description', 'pdf_url', 'is_index', 'address', 'tel', 'email', 'fax']

class CompanyUpdateForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)
    tag = forms.ModelChoiceField(queryset=models.Tag.objects.all())
    video_url = forms.CharField(max_length=128)

    def __init__(self, *args, **kwargs):
        super(CompanyUpdateForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class']='mws-textinput'
        self.fields['pdf_url'].required = False

    def clean_url(self):
        return self.cleaned_data['url'].lower()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not "@" in email or not '.' in email:
            raise forms.ValidationError('Email is not valid')
        return email

    def clean_tel(self):
        tel = self.cleaned_data['tel']
        if not tel.isdecimal():
            raise forms.ValidationError('Telephone number must be all digits')
        return tel

    def clean_fax(self):
        fax = self.cleaned_data['fax']
        if not fax.isdecimal():
            raise forms.ValidationError('Fax number must be all digits')
        return fax

    def clean_video_url(self):
        url = str(self.cleaned_data['video_url'])
        if not url.startswith("http://") and not url.startswith("https://"):
            raise forms.ValidationError('Video Url must be start with http:// or https://')
        return url

    class Meta:
        model = models.Company
        fields = ['name', 'slogan', 'url', 'description', 'pdf_url', 'is_index', 'address', 'tel', 'email', 'fax']


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
