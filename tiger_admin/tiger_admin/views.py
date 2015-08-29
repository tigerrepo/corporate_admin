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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
import logging

logger = logging.getLogger('main')

def check_account_permission(user):
    login_account = get_object_or_404(models.Account, username=user)
    return login_account.account_type == models.Account.ACCOUNT_TYPE_ADMIN

def home(request):
    return render(request, 'base.html')

@user_passes_test(check_account_permission)
def admin_list(request):
    users = models.Account.objects.all()

    request.session['account_type']
    return render_to_response(
        'admins.html',
        {
            'page_title': 'Admins',
            'users': users,
            'account_type': dict(models.Account.ACCOUNT_TYPE_CHOICES)
        },
        context_instance=RequestContext(request)
    )

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
        # salt =  generate_random_password(length=8)

        models.Account.objects.create(
            username=username,
            email=email,
            password=password,
            salt='',
            account_type=account_type)
        logger.info("Account %s, %s has been created by %s", username, password, request.user)
    return redirect('/admin')

class AccountDetailView(DetailView):
    model = models.Account
    template_name = 'admin_detail.html'

class AccountUpdateView(UpdateView):
    pass

class AccountDeleteView(DeleteView):
    pass

class AccountPasswordResetView(View):
    pass

class AccountCompanyListView(ListView):
    pass
