from django import forms
from django.forms.utils import ErrorList
import models
from ckeditor.widgets import CKEditorWidget



class AccountPasswordResetForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password_confirm = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(AccountPasswordResetForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class'] = 'mws-textinput'

    def on_password_differnt_error(self):
        self.errors['new_password'] = ErrorList(['Confirm password is not the same as new password'])
        self.errors['new_password_confirm'] = ErrorList(['Confirm password is not the same as new password'])

    def on_password_incorrect(self):
        self.errors['old_password'] = ErrorList(['Old password is not correct'])

    class Meta:
        model = models.Account
        fields = []


class CompanyCreateForm(forms.ModelForm):
    tag = forms.ModelChoiceField(queryset=models.Tag.objects.all())
    account = forms.ModelChoiceField(queryset=models.Account.objects.filter(status=models.Account.STATUS_ENABLE))
    slogan = forms.CharField(required=False)
    url = forms.CharField(required=False)
    address = forms.CharField(required=False)
    logo_url = forms.FileField(required=False)
    email = forms.CharField(required=False)
    description = forms.CharField(widget=CKEditorWidget(), required=False)

    def __init__(self, *args, **kwargs):
        super(CompanyCreateForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class'] = 'mws-textinput'
        # self.fields['name'].widget.attrs['placeholder'] = 'Please input the company name'
        # self.fields['slogan'].widget.attrs['placeholder'] = 'Please input the company slogan'
        # self.fields['description'].widget.attrs['placeholder'] = 'Please input the company description'
        # self.fields['address'].widget.attrs['placeholder'] = 'Please input the company address'
        # self.fields['tel'].widget.attrs['placeholder'] = 'Please input the company telephone'
        # self.fields['email'].widget.attrs['placeholder'] = 'Please input the company email'
        # self.fields['fax'].widget.attrs['placeholder'] = 'Please input the company fax'
        # self.fields['fax'].required = False
        # self.fields['description'].required = False
        # self.fields['logo_url'].required = False
        # self.fields['tel_opt'].required = False
        # self.fields['open_from'].required = False
        # self.fields['open_to'].required = False

    # def clean_url(self):
    #     return self.cleaned_data['url'].lower()

    def clean_email(self):
        email = self.cleaned_data['email']
        if email == '':
            return email

        if "@" not in email or '.' not in email:
            raise forms.ValidationError('Email is not valid')
        return email
    class Meta:
        model = models.Company
        fields = ['name', 'slogan', 'url', 'description', 'is_index',
                  'address',  'email', 'account', 'dis_order', 'logo_url' ]


class CompanyUpdateForm(forms.ModelForm):
    tag = forms.ModelChoiceField(queryset=models.Tag.objects.all())
    account = forms.ModelChoiceField(queryset=models.Account.objects.filter(status=models.Account.STATUS_ENABLE))
    slogan = forms.CharField(required=False)
    url = forms.CharField(required=False)
    address = forms.CharField(required=False)
    logo_url = forms.FileField(required=False)
    email = forms.CharField(required=False)
    description = forms.CharField(widget=CKEditorWidget(), required=False)

    def __init__(self, *args, **kwargs):
        super(CompanyUpdateForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class'] = 'mws-textinput'
       
    def clean_email(self):
        email = self.cleaned_data['email']
        if email == '':
            return email

        if "@" not in email or '.' not in email:
            raise forms.ValidationError('Email is not valid')
        return email
    class Meta:
        model = models.Company
        fields = ['name', 'slogan', 'url', 'description', 'is_index', 'address',
                  'email', 'account', 'dis_order', 'logo_url']


class CategoryCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryCreateForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class'] = 'mws-textinput'

    class Meta:
        model = models.Tag
        fields = ['name', 'class_name', 'status']


class ProductCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductCreateForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class'] = 'mws-textinput'

    class Meta:
        model = models.Product
        fields = ['company', 'name', 'description']

    def on_duplicate(self):
        self.errors['name'] = ErrorList(['The name is already exists.'])


class GalleryUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GalleryUploadForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class'] = 'mws-textinput'

    class Meta:
        model = models.Gallery
        fields = ['image_url', 'name']

    def on_duplicate_error(self):
        self.errors['name'] = ErrorList(['Image Name is duplicated with existing images'])


class PDFCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PDFCreateForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class'] = 'mws-textinput'

    class Meta:
        model = models.PDF
        fields = ['name', 'url']
