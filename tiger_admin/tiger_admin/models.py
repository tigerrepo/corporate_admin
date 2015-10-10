from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Account(models.Model):
    username = models.CharField(max_length=32, unique=True)
    email = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    salt = models.CharField(max_length=32)
    STATUS_ENABLE=1
    STATUS_DISABLE=0
    STATUS_CHOICES = (
        (STATUS_ENABLE, 'Activated'),
        (STATUS_DISABLE, 'Deactivated'),
    )
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    ACCOUNT_TYPE_ADMIN=0
    ACCOUNT_TYPE_CUSTOMER=1
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
        user = User.objects.create_user(username=instance.username, password=instance.password)

        # Add user info
        user.username = instance.username
        user.email = instance.email
        user.save()

class Company(models.Model):
    name = models.CharField(max_length=32, unique=True)
    slogan = models.CharField(max_length=128)
    url = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=256)
    create_time = models.DateTimeField(auto_now_add=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    status = models.SmallIntegerField(choices=Account.STATUS_CHOICES, default=0)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)

    class Meta:
        db_table = "company_tab"

class Video(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=128)
    video_url = models.CharField(max_length=256)
    host_url = models.CharField(max_length=128)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    class Meta:
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
    name = models.CharField(max_length=32, unique=True)

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
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    create_date = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(choices=Account.STATUS_CHOICES, default=0)

    class Meta:
        unique_together = ('company', 'name')
        db_table = 'product_tab'

    def __unicode__(self):
        return self.name

class Gallery(models.Model):
    name = models.CharField(max_length=64)
    image_url = models.CharField(max_length=64)
    is_cover = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('name', 'product')
        db_table = 'gallery_tab'

    def __unicode__(self):
        return self.name

