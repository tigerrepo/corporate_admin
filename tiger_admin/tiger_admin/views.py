import collections
import logging
import string

import django
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Q
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import (get_object_or_404, redirect, render,
                              render_to_response)
from django.template import RequestContext
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, DeleteView, UpdateView)
from django.views.generic.list import ListView
from utils import generate_random_password, upload_image

import forms
import models
import settings

logger = logging.getLogger('main')


def check_account_permission(user):
    login_account = get_object_or_404(models.Account, username=user.username)
    return login_account.account_type == models.Account.ACCOUNT_TYPE_ADMIN


@login_required
def home(request):
    return render(request, 'base.html')


@login_required
def admin_list(request):
    account = models.Account.objects.get(username=request.user.username)
    is_admin = account.account_type == models.Account.ACCOUNT_TYPE_ADMIN
    if is_admin:
        if request.user.is_superuser:
            users = models.Account.objects.exclude(username=request.user.username)
        else:
            users = list(models.Account.objects.filter(account_type=models.Account.ACCOUNT_TYPE_CUSTOMER))
            users.append(account)
    else:
        users = [account]

    return render_to_response(
        'admins.html',
        {
            'is_admin' : is_admin,
            'page_title': 'Admins',
            'users': users,
            'is_superuser': request.user.is_superuser
        },
        context_instance=RequestContext(request)
    )


@login_required
@user_passes_test(check_account_permission)
def update_status(request, pk):
    try:
        with transaction.atomic(using="tiger_admin"):
            account = models.Account.objects.get(pk=pk)
            account.status = not account.status
            account.save()

            u = User.objects.get(username=account.username)
            u.is_active = not u.is_active
            u.save()
    except Exception as e:
        logger.error("Account %s updated status fail, roll back.", account.username)
        # add error page
        return redirect(reverse('admin-detail', kwargs={'pk': pk}))

    logger.info("Account %s has been updated status, %s, done by %s",
                account.username, account.status, request.user)
    return redirect(reverse('admin-detail', kwargs={'pk':pk}))


@login_required
def update_company_status(request, pk):
    # check company owner or admin
    company = models.Company.objects.get(pk=pk)
    company.status = not company.status
    company.save()

    logger.info("Website %s has been updated status, %s, done by %s",
                company.name, company.status, request.user)
    return redirect(reverse('company-detail', kwargs={'pk':pk}))


@login_required
def update_pdf_status(request, pk):
    account = models.Account.objects.get(username=request.user)
    companies = [obj for obj in models.Company.objects.filter(account=account)]
    pdf_ids = [obj.id for obj in models.PDF.objects.filter(company__in=companies)]
    if int(pk) in pdf_ids or account.account_type == models.Account.ACCOUNT_TYPE_ADMIN:
        pdf = models.PDF.objects.get(pk=pk)
        pdf.status = not pdf.status
        pdf.save()

        logger.info("PDF %s has been updated status, %s, done by %s",
                    pdf.name, pdf.status, request.user)
    else:
        logger.info("PDF id %s has tried to be updated to status, "
                    "but failed as login user do not have permission, done by %s",
                    pk, request.user)

    return redirect(reverse('pdf-detail', kwargs={'pk': pk}))


@login_required
@user_passes_test(check_account_permission)
def password_reset(request, pk):
    account = models.Account.objects.get(pk=pk)
    password = generate_random_password(length=8)
    u = User.objects.get(username=account.username)
    u.set_password(password)
    u.save()

    logger.info("Account %s has been reset password %s, done by %s",
                account.username, password, request.user)
    if settings.SENT_EMAIL:
        msg_txt = 'Your password is reset to %s, please login and change your password.' % password

        msg = string.join((
            "From: %s" % settings.EMAIL_HOST_USER,
            "To: %s" % account.email,
            "Subject: Notification",
            "",
            msg_txt
            ), "\r\n")

        send_mail('Notification', msg, settings.EMAIL_HOST_USER, [account.email], fail_silently=False)
    return redirect(reverse('admin-detail', kwargs={'pk':pk}))


@login_required
@user_passes_test(check_account_permission)
def admin_add(request):
    username = request.POST['username'].strip()
    email = request.POST['email'].strip()
    account_type = request.POST['account_type']
    try:
        account = models.Account.objects.get(Q(username__exact=username) | Q(email__exact=email))
        if account.status == models.Account.STATUS_DISABLE:
            account.status = models.Account.STATUS_ENABLE
            account.save()
            messages.error(request,
                           'Account %s already exists but is disabled, the status has been changed to enable' %
                           username)
            logger.info("Account %s has been activated by %s", username, request.user)
        else:
            messages.error(request, 'Account %s already exists' % username)

    except models.Account.DoesNotExist:
        password = generate_random_password(length=8)
        models.Account.objects.create(
            username=username,
            email=email,
            password='',
            salt='',
            account_type=account_type)

        u = User.objects.get(username=username)
        u.set_password(password)
        u.save()
        logger.info("Account %s, %s, %s has been created by %s", username, password, account_type, request.user)
        if settings.SENT_EMAIL:
            msg_txt = """ Welcome to Flinter! 

Your profile is generated, please use the email add which you have received this email from as your Username and %s
as password to login. For your safety, please change your password once you login the system.
                      
See you in the community, new Flinter!

Best regards, 

Flinter Team"""

            msg = string.join((
                "From: %s" % settings.EMAIL_HOST_USER,
                "To: %s" % u.email,
                "Subject: Notification" ,
                "",
                msg_txt % password
                ), "\r\n")

            send_mail('Notification', msg, settings.EMAIL_HOST_USER, [u.email], fail_silently=False)

    return redirect('/admin')


class AccountDetailView(DetailView):
    model = models.Account
    template_name = 'admin_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AccountDetailView, self).get_context_data(**kwargs)
        context['login_user'] = self.kwargs['account']
        return context


class AccountDeleteView(DeleteView):
    model = models.Account
    template_name = 'admin_delete_form.html'

    def get_success_url(self):
        logger.info("Account %s has been deleted by %s", self.object.username, self.request.user)
        return reverse('admin-list')


class AccountPasswordResetView(UpdateView):
    model = models.Account
    form_class = forms.AccountPasswordResetForm
    template_name = 'admin_reset_password_form.html'

    def form_valid(self, form):
        account = self.get_object()

        old = form.cleaned_data['old_password']
        new = form.cleaned_data['new_password']
        new_confirm = form.cleaned_data['new_password_confirm']
        if not authenticate(username=account.username, password=old):
            form.on_password_incorrect()
            return self.form_invalid(form)

        if new.strip() != new_confirm.strip():
            form.on_password_differnt_error()
            return self.form_invalid(form)

        u = User.objects.get(username=account.username)
        u.set_password(new)
        u.save()
        logger.info("Reset password success for %s, done by %s.", account.username, self.request.user)

        return redirect(reverse('admin-detail', kwargs={'pk': self.object.pk}))


class AccountCompanyListView(ListView):
    model = models.Company
    template_name = 'company_list.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk', 0)
        context = super(AccountCompanyListView, self).get_context_data(**kwargs)

        account = get_object_or_404(models.Account, pk=pk)
        context['company_list'] = models.Company.objects.filter(account=account)
        context['domain'] = settings.DOMAIN_NAME
        context['is_admin'] = self.kwargs['is_admin']
        return context


class CompanyListView(ListView):
    model = models.Company
    template_name = 'company_list.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyListView, self).get_context_data(**kwargs)

        account = models.Account.objects.get(username__exact=self.request.user.username)
        is_admin = account.account_type == models.Account.ACCOUNT_TYPE_ADMIN
        if is_admin:
            company_list = models.Company.objects.all()
        else:
            company_list = models.Company.objects.filter(account=account)

        company_tag_dict = collections.defaultdict(list)
        for company_tag in models.CompanyTag.objects.select_related("tag").all():
            company_tag_dict[company_tag.company_id].append(company_tag.tag.name)

        company_list_with_tag = []
        for company in company_list:
            company_dict = dict()
            company_dict['name'] = company.name
            company_dict['url'] = company.url
            company_dict['account'] = company.account
            company_dict['status'] = company.get_status_display
            company_dict['pk'] = company.id
            company_dict['create_time'] = company.create_time
            company_dict['is_index'] = company.is_index
            company_dict['tag'] = ','.join(company_tag_dict.get(company.id, []))
            company_dict['dis_order'] = company.dis_order
            company_list_with_tag.append(company_dict)

        context['is_admin'] = is_admin
        context['company_list'] = company_list_with_tag
        context['domain'] = settings.DOMAIN_NAME
        return context


class CompanyCreateView(CreateView):
    model = models.Company
    form_class = forms.CompanyCreateForm
    template_name = 'company_add.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyCreateView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        try:
            with transaction.atomic(using='tiger_admin'):
                obj = form.save()

                if form.cleaned_data['logo_url'] is not None:
                    directory = '%s%s' % (settings.LOGO_ROOT, obj.id)
                    logo_url = upload_image(form.cleaned_data['logo_url'], directory)
                    obj.logo_url = logo_url

                    obj.save()

                # video_url = form.cleaned_data['video_url']
                # name = video_url.split("=")[-1]
                # models.Video.objects.create(
                #     name=name,
                #     description='',
                #     video_url=video_url,
                #     host_url='%s/%s.mp4' % (obj.id, obj.id),
                #     company=obj)

                tag = form.cleaned_data['tag']
                models.CompanyTag.objects.get_or_create(company=obj, tag=tag)
        except Exception as e:
            logger.error("create Website fail, roll back, website %s, operate by %s. Exception: %s",
                         form.cleaned_data['name'], self.request.user, str(e))
            # add error in page
            return super(CompanyCreateView, self).form_invalid(form)

        logger.info("Website %s has been created by %s", form.cleaned_data['name'], self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('company-list')


class CompanyDetailView(DetailView):
    model = models.Company
    template_name = 'company_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyDetailView, self).get_context_data(**kwargs)
        context['domain'] = settings.DOMAIN_NAME
        is_admin = self.kwargs['is_admin']

        company_tag_dict = collections.defaultdict(list)
        for company_tag in models.CompanyTag.objects.select_related("tag").all():
            company_tag_dict[company_tag.company_id].append(company_tag.tag.name)

        context['tag'] = ','.join(company_tag_dict.get(self.object.pk, []))

        if self.get_object().logo_url:
            context['logo_url'] = '%s%s/%s' % (settings.LOGO_URL, self.get_object().id, self.get_object().logo_url)
        else:
            context['logo_url'] = ''

        # try:
        #     video = models.Video.objects.get(company=self.get_object())
        #     context['youtube_url'] = "%s%s" % (settings.YOUTUBE_URL_PREFIX, video.name)
        # except models.Video.DoesNotExist:
        #     context['youtube_url'] = ''

        return context


class CompanyUpdateView(UpdateView):
    model = models.Company
    form_class = forms.CompanyUpdateForm
    template_name = 'company_update.html'

    def get_initial(self):

        # video = get_object_or_404(models.Video, company=self.object)
        try:
            tag = models.CompanyTag.objects.get(company=self.object)
            tag_val = tag.tag_id
        except Exception as e:
            tag_val = 0
        initials = dict()
        # initials['video_url'] = video.video_url
        initials['tag'] = tag_val
        return initials

    def get_context_data(self, **kwargs):
        context = super(CompanyUpdateView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        try:
            with transaction.atomic(using='tiger_admin'):
                if form.cleaned_data['dis_order'] is None:
                    form.instance.dis_order = self.object.dis_order
                if not form.instance.dis_order:
                    form.instance.dis_order = 0

                obj = form.save()

                if form.cleaned_data['logo_url'] is not None:
                    if form.cleaned_data['logo_url'] != obj.logo_url:
                        directory = '%s%s' % (settings.LOGO_ROOT, obj.id)
                        logo_url = upload_image(form.cleaned_data['logo_url'], directory)
                        obj.logo_url = logo_url
                        obj.save()

                # try:
                #     video = models.Video.objects.get(company=obj)
                #     if form.cleaned_data['video_url'] != video.video_url:
                #         video_url = form.cleaned_data['video_url']
                #         name = video_url.split("=")[-1]
                #         models.Video.objects.filter(company=obj).update(
                #                 name=name,
                #                 description='',
                #                 video_url=video_url,
                #                 host_url='%s/%s.mp4' % (obj.id, obj.id))
                # except models.Video.DoesNotExist:
                #         video_url = form.cleaned_data['video_url']
                #         name = video_url.split("=")[-1]
                #         models.Video.objects.filter(company=obj).update(
                #                 name=name,
                #                 description='',
                #                 video_url=video_url,
                #                 host_url='%s/%s.mp4' % (obj.id, obj.id))

                tag = form.cleaned_data['tag']
                models.CompanyTag.objects.filter(company=obj).update(tag=tag)
        except Exception as e:
            logger.error("update Website fail, roll back, website %s, operate by %s. Exception: %s",
                         form.cleaned_data['name'], self.request.user, str(e))
            # add error in page
            return super(CompanyUpdateView, self).form_invalid(form)

        logger.info("Website %s has been updated by %s", form.cleaned_data['name'], self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('company-detail', kwargs={'pk': self.object.pk})


class CompanyDeleteView(DeleteView):
    model = models.Company
    template_name = 'company_delete_form.html'

    def get_success_url(self):
        logger.info("Website %s has been deleted by %s", self.object.name, self.request.user)
        return reverse('company-list')


class CompanyProductListView(ListView):
    model = models.Product
    template_name = 'product_list.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyProductListView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        company = get_object_or_404(models.Company, pk=pk)
        context['object_list'] = models.Product.objects.filter(company=company)
        context['can_add'] = self.kwargs['is_superuser'] or self.kwargs['is_owner']
        return context


class CompanyMessageListView(ListView):
    model = models.Contact
    template_name = 'message_list.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyMessageListView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        company = get_object_or_404(models.Company, pk=pk)
        context['object_list'] = models.Contact.objects.filter(company=company)
        return context


class CompanyPDFListView(ListView):
    model = models.PDF
    template_name = 'pdf_list.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyPDFListView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        company = get_object_or_404(models.Company, pk=pk)
        context['object_list'] = models.PDF.objects.filter(company=company)
        context['can_add'] = self.kwargs['is_superuser'] or self.kwargs['is_owner']
        context['pk'] = pk
        return context


class MessageListView(ListView):
    model = models.Contact
    template_name = 'message_list.html'

    def get_context_data(self, **kwargs):
        context = super(MessageListView, self).get_context_data(**kwargs)
        account = models.Account.objects.get(username=self.request.user.username)
        is_admin = account.account_type == models.Account.ACCOUNT_TYPE_ADMIN
        context['is_admin'] = is_admin
        if is_admin:
            context['object_list'] = models.Contact.objects.all()
        else:
            companies = models.Company.objects.filter(account=account)
            context['object_list'] = models.Contact.objects.filter(company__in=companies)
        return context


class MessageDetailView(DetailView):
    model = models.Contact
    template_name = 'message_detail.html'


class CategoryCreateView(CreateView):
    model = models.Tag
    form_class = forms.CategoryCreateForm
    template_name = 'category_add.html'

    def get_success_url(self):
        logger.info("Category %s has been updated by %s", self.object.name, self.request.user)
        return reverse('category-list')


class CategoryListView(ListView):
    model = models.Tag
    template_name = 'category_list.html'


class CategoryDetailView(DetailView):
    model = models.Tag
    template_name = 'category_detail.html'


class CategoryDeleteView(DeleteView):
    model = models.Tag
    template_name = 'category_delete_form.html'

    def delete(self, request, *args, **kwargs):
        try:
            name = self.get_object().name
            self.get_object().delete()
            logger.info("Category %s has been deleted by %s", name, self.request.user)
            return HttpResponseRedirect(self.get_success_url())

        except Exception as e:
            messages.error(request,
                           'Delete category failed, there are corporates with this tag exists')
            return HttpResponseRedirect(reverse('category-detail', kwargs={"pk": self.get_object().id}))

    def get_success_url(self):
        return reverse('category-list')


class CategoryUpdateView(UpdateView):
    model = models.Tag
    form_class = forms.CategoryCreateForm
    template_name = 'category_update.html'

    def get_success_url(self):
        logger.info("Category %s has been updated by %s", self.object.name, self.request.user)
        return reverse('category-detail', kwargs={'pk': self.object.pk})


class ProductCreateView(CreateView):
    model = models.Product
    form_class = forms.ProductCreateForm
    template_name = 'product_add.html'

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        account = models.Account.objects.get(username=self.request.user.username)
        is_admin = account.account_type == models.Account.ACCOUNT_TYPE_ADMIN
        if not is_admin:
            context['form'].fields['company'].queryset = models.Company.objects.filter(account=account)
        return context

    def form_valid(self, form):
        try:
            obj = form.save()
            logger.info("Product %s has been created by %s", obj.name, self.request.user)
            return HttpResponseRedirect(self.get_success_url())
        except IntegrityError:
            form.on_duplicate()
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('product-list')


class ProductListView(ListView):
    model = models.Product
    template_name = 'product_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)

        account = models.Account.objects.get(username__exact=self.request.user.username)
        is_admin = account.account_type == models.Account.ACCOUNT_TYPE_ADMIN
        if not is_admin:
            companies = list(c.id for c in models.Company.objects.filter(account=account))
            context['object_list'] = models.Product.objects.filter(company_id__in=companies)
        context['can_add'] = self.request.user.is_superuser or not is_admin
        return context


class ProductDetailView(DetailView):
    model = models.Product
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        models.Account.objects.get(username=self.request.user.username)
        return context


class ProductDeleteView(DeleteView):
    model = models.Product
    template_name = 'product_delete_form.html'

    def delete(self, request, *args, **kwargs):
        try:
            name = self.get_object().name
            self.get_object().delete()
            logger.info("Product %s has been deleted by %s", name, self.request.user)
            return HttpResponseRedirect(self.get_success_url())
        except Exception as e:
            messages.error(request,
                           'Delete product failed, there are images in this product.')
            return HttpResponseRedirect(reverse('product-detail', kwargs={"pk": self.get_object().id}))

    def get_success_url(self):
        return reverse('product-list')


class ProductUpdateView(UpdateView):
    model = models.Product
    form_class = forms.ProductCreateForm
    template_name = 'product_update.html'

    def get_success_url(self):
        logger.info("Product %s has been updated by %s", self.get_object().name, self.request.user)
        return reverse('product-detail', kwargs={'pk': self.get_object().pk})


class ProductImageListView(ListView):
    model = models.Gallery
    template_name = 'gallery_list.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk', 0)
        context = super(ProductImageListView, self).get_context_data(**kwargs)
        context['gallery_list'] = models.Gallery.objects.filter(product_id=pk)
        context['product'] = pk
        context['url_prefix'] = settings.IMAGE_URL_PREFIX
        context['is_admin'] = self.kwargs['is_admin']
        return context


class GalleryDetailView(DetailView):
    model = models.Gallery
    template_name = 'gallery_detail.html'

    def get_context_data(self, **kwargs):
        context = super(GalleryDetailView, self).get_context_data(**kwargs)
        context['url_prefix'] = settings.IMAGE_URL_PREFIX
        return context


class GalleryCreateView(CreateView):
    model = models.Gallery
    form_class = forms.GalleryUploadForm
    template_name = 'gallery_add.html'

    def form_valid(self, form):
        try:
            pk = self.kwargs.get('pk', 0)
            product = get_object_or_404(models.Product, pk=pk)
            directory = '%s%s' % (settings.MEDIA_ROOT, pk)
            image_url = upload_image(form.cleaned_data['image_url'], directory)
            form.instance.image_url = image_url
            form.instance.product = product
            form.save()
        except IntegrityError:
            form.on_duplicate_error()
            return self.form_invalid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        pk = self.kwargs.get('pk', 0)
        logger.info("Image has been uploaded by %s", self.request.user)
        return reverse('product-image-list', kwargs={'pk': pk})


class GalleryDetailView(DetailView):
    model = models.Gallery
    template_name = 'gallery_detail.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('ppk', 0)
        context = super(GalleryDetailView, self).get_context_data(**kwargs)
        context['url_prefix'] = settings.IMAGE_URL_PREFIX
        context['product'] = pk
        return context


class GalleryDeleteView(DeleteView):
    model = models.Gallery
    template_name = 'gallery_delete_form.html'

    def get_success_url(self):
        pk = self.kwargs.get('ppk', 0)
        logger.info("Image %s has been deleted by %s", self.object.name, self.request.user)
        return reverse('product-image-list', kwargs={'pk': pk})


class GalleryUpdateView(UpdateView):
    model = models.Gallery
    form_class = forms.GalleryUploadForm
    template_name = 'gallery_update.html'

    def form_valid(self, form):
        try:
            pk = self.kwargs.get('ppk', 0)

            if form.cleaned_data['image_url'] is not None:
                if form.cleaned_data['image_url'] != self.get_object().image_url:
                    directory = '%s%s' % (settings.MEDIA_ROOT, pk)
                    image_url = upload_image(form.cleaned_data['image_url'], directory)
                    form.instance.image_url = image_url
            form.save()
        except IntegrityError:
            form.on_duplicate_error()
            return self.form_invalid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        pk = self.kwargs.get('ppk', 0)
        logger.info("Image %s has been updated by %s", self.object.id, self.request.user)
        return reverse('gallery-detail', kwargs={'ppk': pk, 'pk':self.object.pk})


class EnquiresListView(ListView):
    model = models.Enquiry
    template_name = 'enqury_list.html'


class PDFCreateView(CreateView):
    model = models.PDF
    form_class = forms.PDFCreateForm
    template_name = 'pdf_add.html'

    def get_context_data(self, **kwargs):
        context = super(PDFCreateView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.company_id = self.kwargs['pk']
        if form.cleaned_data['url'] is not None:
            directory = '%s%s' % (settings.PDF_ROOT, self.kwargs['pk'])
            pdf_url = upload_image(form.cleaned_data['url'], directory)
            form.instance.url = pdf_url
            obj = form.save()
            logger.info("PDF %s has been created by %s", obj.name, self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('company-pdf-list', kwargs={'pk': self.kwargs['pk']})


class PDFDetailView(DetailView):
    model = models.PDF
    template_name = 'pdf_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PDFDetailView, self).get_context_data(**kwargs)
        context['url'] = '%s%s/%s' % (settings.PDF_URL, self.object.company_id, self.object.url)
        return context


class PDFUpdateView(UpdateView):
    model = models.PDF
    form_class = forms.PDFCreateForm
    template_name = 'pdf_update.html'

    def get_context_data(self, **kwargs):
        context = super(PDFUpdateView, self).get_context_data(**kwargs)
        context['url'] = '%s%s/%s' % (settings.PDF_URL, self.object.company_id, self.object.url)
        return context

    def form_valid(self, form):
        obj = form.save()
        if form.cleaned_data['url'] is not None:
            if form.cleaned_data['url'] != obj.url:
                directory = '%s%s' % (settings.PDF_ROOT, obj.id)
                pdf_url = upload_image(form.cleaned_data['url'], directory)
                obj.url = pdf_url
                obj.save()

        logger.info("PDF %s has been created by %s", obj.name, self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('company-pdf-list', kwargs={'pk': self.object.company_id})