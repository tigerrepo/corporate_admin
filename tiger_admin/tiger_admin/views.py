from django.shortcuts import render
from tiger_admin import models
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages
from utils import format_date, generate_random_password
import hashlib
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from tiger_admin import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail
import logging
from tiger_admin import settings
from django.db import transaction

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
        users = models.Account.objects.filter(account_type=models.Account.ACCOUNT_TYPE_CUSTOMER)
    else:
        users = [account]

    return render_to_response(
        'admins.html',
        {
            'is_admin' : is_admin,
            'page_title': 'Admins',
            'users': users,
            'account_type': dict(models.Account.ACCOUNT_TYPE_CHOICES)
        },
        context_instance=RequestContext(request)
    )

@login_required
@user_passes_test(check_account_permission)
def update_status(request, pk):
    with transaction.atomic():
        account = models.Account.objects.get(pk=pk)
        account.status = not account.status
        account.save()

        u = User.objects.get(username=account.username)
        u.is_active = not u.is_active
        u.save()

    logger.info("Account %s has been updated status, %s, done by %s",
                account.username, account.status, request.user)
    return redirect(reverse('admin-detail', kwargs={'pk':pk}))

def update_company_status(request, pk):
    company = models.Company.objects.get(pk=pk)
    company.status = not company.status
    company.save()

    logger.info("Website %s has been updated status, %s, done by %s",
                company.name, company.status, request.user)
    return redirect(reverse('company-detail', kwargs={'pk':pk}))

@login_required
@user_passes_test(check_account_permission)
def password_reset(request, pk):
    account = models.Account.objects.get(pk=pk)
    password = generate_random_password(length=8)
    u = User.objects.get(username=account.username)
    u.set_password(password)
    u.save()

    logger.info("Account %s has been reset password, done by %s",
                account.username, request.user)
    if settings.SENT_EMAIL:
        send_mail('TEST SUB', 'message', settings.EMAIL_HOST_USER,
                [settings.DEFAULT_TO_EMAIL], fail_silently=False)
    return redirect(reverse('admin-detail', kwargs={'pk':pk}))


@login_required
@user_passes_test(check_account_permission)
def admin_add(request):
    username = request.POST['username'].strip()
    email = request.POST['email'].strip()
    account_type = request.POST['account_type']
    try:
        account = models.Account.objects.get(username__exact=username)
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
    return redirect('/admin')

class AccountDetailView(DetailView):
    model = models.Account
    template_name = 'admin_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AccountDetailView, self).get_context_data(**kwargs)
        account = models.Account.objects.get(username=self.request.user.username)
        context['login_user'] = account
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
        return context

class CompanyListView(ListView):
    model = models.Company
    template_name = 'company_list.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyListView, self).get_context_data(**kwargs)

        account = models.Account.objects.get(username=self.request.user.username)

        is_admin = account.account_type == models.Account.ACCOUNT_TYPE_ADMIN
        if is_admin:
            company_list = models.Company.objects.all()
        else:
            company_list = models.Company.objects.filter(account=account)
        context['is_admin'] = is_admin
        context['company_list'] = company_list
        context['domain'] = settings.DOMAIN_NAME
        return context

class CompanyCreateView(CreateView):
    model = models.Company
    form_class = forms.CompanyCreateForm
    template_name = 'company_add.html'

    def form_valid(self, form):
        account = models.Account.objects.get(username__exact=self.request.user.username)
        form.instance.account = account
        logger.info("Website %s has been created by %s", form.cleaned_data['name'], self.request.user)
        return super(CompanyCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('company-list')

class CompanyDetailView(DetailView):
    model = models.Company
    template_name = 'company_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyDetailView, self).get_context_data(**kwargs)
        context['domain'] = settings.DOMAIN_NAME
        account = models.Account.objects.get(username=self.request.user.username)
        is_admin = account.account_type == models.Account.ACCOUNT_TYPE_ADMIN
        context['is_admin'] = is_admin
        return context

class CompanyUpdateView(UpdateView):
    model = models.Company
    form_class = forms.CompanyCreateForm
    template_name = 'company_update.html'

    def get_success_url(self):
        logger.info("Website %s has been updated by %s", self.object.name, self.request.user)
        return reverse('company-detail', kwargs={'pk': self.object.pk})

class CompanyDeleteView(DeleteView):
    model = models.Company
    template_name = 'company_delete_form.html'

    def get_success_url(self):
        logger.info("Website %s has been deleted by %s", self.object.name, self.request.user)
        return reverse('company-list')

class CompanyProductListView(ListView):
    pass

class CompanyVideoListView(ListView):
    pass

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

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        account = models.Account.objects.get(username=self.request.user.username)
        is_admin = account.account_type == models.Account.ACCOUNT_TYPE_ADMIN
        context['is_admin'] = is_admin
        return context

class CategoryDetailView(DetailView):
    model = models.Tag
    template_name = 'category_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        account = models.Account.objects.get(username=self.request.user.username)
        is_admin = account.account_type == models.Account.ACCOUNT_TYPE_ADMIN
        context['is_admin'] = is_admin
        return context

class CategoryDeleteView(DeleteView):
    model = models.Tag
    template_name = 'category_delete_form.html'

    def get_success_url(self):
        logger.info("Category %s has been deleted by %s", self.object.name, self.request.user)
        return reverse('category-list')

class CategoryUpdateView(UpdateView):
    model = models.Tag
    form_class = forms.CategoryCreateForm
    template_name = 'category_update.html'

    def get_success_url(self):
        logger.info("Category %s has been updated by %s", self.object.name, self.request.user)
        return reverse('category-detail', kwargs={'pk': self.object.pk})

