from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import localtime, now


class Account(models.Model):
    username = models.CharField(max_length=32, unique=True)
    email = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    salt = models.CharField(max_length=32)
    STATUS_ENABLE = 1
    STATUS_DISABLE = 0
    STATUS_CHOICES = (
        (STATUS_ENABLE, 'Activated'),
        (STATUS_DISABLE, 'Deactivated'),
    )
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    ACCOUNT_TYPE_ADMIN = 0
    ACCOUNT_TYPE_CUSTOMER = 1
    ACCOUNT_TYPE_CHOICES = (
        (ACCOUNT_TYPE_CUSTOMER, u'Customer Admin'),
        (ACCOUNT_TYPE_ADMIN, u'System Admin'),
    )
    account_type = models.SmallIntegerField(choices=ACCOUNT_TYPE_CHOICES, default=1)

    class Meta:
        db_table = "account_tab"

    def __unicode__(self):
        return self.username


@receiver(pre_save, sender=Account)
def create_user_if_not_exist(sender, **kwargs):
    instance = kwargs.get('instance')
    try:
        # Check if a user with the same username exists
        user = User.objects.get(username__exact=instance.username)

        user.email = instance.email
        user.save()

    except User.DoesNotExist:
        user = User.objects.create_user(username=instance.username, password=instance.password,
                                        last_login=localtime(now()))

        # Add user info
        user.username = instance.username
        user.email = instance.email
        user.save()


@receiver(post_delete, sender=Account)
def delete_user(sender, instance=None, **kwargs):
    try:
        user = User.objects.get(username__exact=instance.username)
    except User.DoesNotExist:
        pass
    else:
        user.delete()


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slogan = models.CharField(max_length=128)
    url = models.CharField(max_length=64, unique=True)
    # description = models.CharField(max_length=1024)
    description = RichTextField()
    create_time = models.DateTimeField(auto_now_add=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    status = models.SmallIntegerField(choices=Account.STATUS_CHOICES, default=Account.STATUS_DISABLE)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    # pdf_url = models.FileField(upload_to='pdf', max_length=64)
    is_index = models.BooleanField(default=False)
    address = models.CharField(max_length=128)
    email = models.CharField(max_length=64)
    tel = models.CharField(max_length=20)
    fax = models.CharField(max_length=20)
    dis_order = models.IntegerField(default=0)
    logo_url = models.FileField(upload_to='logo', max_length=64)
    tel_opt = models.CharField(max_length=20, default='')
    open_from = models.CharField(max_length=20, default='')
    open_to = models.CharField(max_length=20, default='')

    class Meta:
        db_table = "company_tab"

    def __unicode__(self):
        return self.name


class Video(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    video_url = models.CharField(max_length=256)
    host_url = models.CharField(max_length=128)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('name', 'company')
        db_table = "video_tab"


class Contact(models.Model):
    sender = models.CharField(max_length=32)
    mobile = models.CharField(max_length=20)
    email = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=512)
    create_date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    class Meta:
        db_table = 'contact_tab'

    def __unicode__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    class_name = models.CharField(max_length=64, unique=True)
    status = models.SmallIntegerField(choices=Account.STATUS_CHOICES, default=1)

    class Meta:
        db_table = 'tag_tab'

    def __unicode__(self):
        return self.name


class CompanyTag(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('company', 'tag')
        db_table = 'company_tag_tab'


class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    description = RichTextField()
    create_date = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(choices=Account.STATUS_CHOICES, default=1)

    class Meta:
        db_table = 'product_tab'

    def __unicode__(self):
        return self.name


class Gallery(models.Model):
    name = models.CharField(max_length=64)
    image_url = models.ImageField(upload_to='gallery/%Y%m%d', max_length=64)
    is_cover = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    class Meta:
        db_table = 'gallery_tab'

    def __unicode__(self):
        return self.name


class Enquiry(models.Model):
    name = models.CharField(max_length=64)
    company = models.CharField(max_length=128)
    email = models.CharField(max_length=64)
    mobile = models.CharField(max_length=20)
    REGION_TYPE_SG = 0
    REGION_TYPE_CN = 1
    REGION_TYPE_CHOICES = (
        (REGION_TYPE_SG, u'Singapore'),
        (REGION_TYPE_CN, u'China'),
    )
    region = models.SmallIntegerField(choices=REGION_TYPE_CHOICES, default=0)
    ip = models.CharField(max_length=64)
    create_time = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=256)

    class Meta:
        db_table = 'enquiry_tab'

    def __unicode__(self):
        return self.name


class HotCompany(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    dis_order = models.IntegerField(default=1)

    class Meta:
        db_table = 'hot_company_tab'


class PDF(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=64)
    url = models.FileField(upload_to='pdf', max_length=128)
    status = models.SmallIntegerField(choices=Account.STATUS_CHOICES, default=1)

    class Meta:
        db_table = 'pdf_tab'
