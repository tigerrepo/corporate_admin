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

def home(request):
    return render(request, 'base.html')

def login(request):
    return render(request, 'login.html')

def logout(request):
    return render(request, 'login.html')

def admin_list(request):
    users = models.Account.objects.all()

    return render_to_response(
        'admins.html',
        {
            'page_title': 'Admins',
            'users': users,
            'account_type': dict(models.Account.ACCOUNT_TYPE_CHOICES)
        },
        context_instance=RequestContext(request)
    )

def admin_add(request):
    username = request.POST['username'].strip()
    email = request.POST['email'].strip()
    account_type = request.POST['account_type']
    print username, email, account_type
    try:
        account = models.Account.objects.get(email__exact=email)
        if account.status == models.Account.STATUS_DISABLE:
            account.status = models.Account.STATUS_ENABLE
            account.save()
            messages.error(request,
                           'Account %s already exists but is disabled, the status has been changed to enable' %
                           email)
        else:
            messages.error(request, 'Account %s already exists' % email)

    except models.Account.DoesNotExist:
        password = generate_random_password(length=8)
        salt =  generate_random_password(length=8)

        models.Account.objects.create(
            username=username,
            email=email,
            password=hashlib.md5(password + salt).hexdigest(),
            salt=salt,
            account_type=account_type)
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
