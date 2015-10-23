from django.conf.urls import patterns, include, url
from django.http import HttpResponseForbidden
from tiger_admin import views, models
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

def check_user_role(func):
    def wrap(request, *args, **kwargs):
        try:
            account_pk = int(kwargs.get('pk', 0))
            account = models.Account.objects.get(username__exact=request.user.username)
            if account.id == account_pk or account.account_type == models.Account.ACCOUNT_TYPE_ADMIN:
                kwargs['is_admin'] = account.account_type == models.Account.ACCOUNT_TYPE_ADMIN
                kwargs['account'] = account
                return func(request, *args, **kwargs)
        except models.Account.DoesNotExist:
            return HttpResponseForbidden()
        return HttpResponseForbidden()
    return wrap

def check_corporate_permission(func):
    def wrap(request, *args, **kwargs):
        try:
            corporate_pk = int(kwargs.get('pk', 0))
            account = models.Account.objects.get(username__exact=request.user.username)
            kwargs['is_admin'] = account.account_type == models.Account.ACCOUNT_TYPE_ADMIN
            kwargs['account'] = account
            if kwargs['is_admin'] or models.Company.objects.get(pk=corporate_pk, account=account):
                return func(request, *args, **kwargs)
        except models.Company.DoesNotExist:
            return HttpResponseForbidden()
        return HttpResponseForbidden()
    return wrap

def check_product_permission(func):
    def wrap(request, *args, **kwargs):
        try:
            pk = int(kwargs.get('pk', 0))
            account = models.Account.objects.get(username__exact=request.user.username)
            kwargs['is_admin'] = account.account_type == models.Account.ACCOUNT_TYPE_ADMIN
            kwargs['account'] = account
            companies = list(c.id for c in models.Company.objects.filter(account=account))
            if kwargs['is_admin'] or models.Product.objects.get(pk=pk, company__in=companies):
                return func(request, *args, **kwargs)
        except models.Product.DoesNotExist:
            return HttpResponseForbidden()
        return HttpResponseForbidden()
    return wrap

def check_gallery_permission(func):
    def wrap(request, *args, **kwargs):
        try:
            corporate_pk = int(kwargs.get('pk', 0))
            account = models.Account.objects.get(username__exact=request.user.username)
            kwargs['is_admin'] = account.account_type == models.Account.ACCOUNT_TYPE_ADMIN
            kwargs['account'] = account
            companies = list(c.id for c in models.Company.objects.filter(account=account))
            products = list(p.id for p in models.Product.objects.filter(company__in=companies))
            if kwargs['is_admin'] or models.Gallery.objects.get(pk=pk, product__in=products):
                return func(request, *args, **kwargs)
        except models.Gallery.DoesNotExist:
            return HttpResponseForbidden()
        return HttpResponseForbidden()
    return wrap


def check_message_permission(func):
    def wrap(request, *args, **kwargs):
        try:
            pk = int(kwargs.get('pk', 0))
            account = models.Account.objects.get(username__exact=request.user.username)
            kwargs['is_admin'] = account.account_type == models.Account.ACCOUNT_TYPE_ADMIN
            kwargs['account'] = account
            if models.Contact.objects.get(pk=pk, account=account):
                return func(request, *args, **kwargs)
        except models.Contact.DoesNotExist:
            return HttpResponseForbidden()
        return HttpResponseForbidden()
    return wrap



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tiger_admin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'tiger_admin.views.home', name='home'),
    url(r'^login/$', auth_views.login, {'template_name':'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name':'logout.html'},name='logout'),

    # admin
    url(r'^admin/$', 'tiger_admin.views.admin_list', name='admin-list'),
    url(r'^admin/add/$', 'tiger_admin.views.admin_add', name='admin-add'),
    url(r'^admin/(?P<pk>\d+)/detail/$',
        check_user_role(login_required(views.AccountDetailView.as_view())),
        name='admin-detail'),
    url(r'^admin/(?P<pk>\d+)/update_status/$', 'tiger_admin.views.update_status', name='admin-update-status'),
    url(r'^admin/(?P<pk>\d+)/delete/$',
        check_user_role(login_required(views.AccountDeleteView.as_view())),
        name='admin-delete'),
    url(r'^admin/(?P<pk>\d+)/password_change/$',
        check_user_role(login_required(views.AccountPasswordResetView.as_view())),
        name='admin-change-password'),
    url(r'^admin/(?P<pk>\d+)/password_reset/$', 'tiger_admin.views.password_reset', name='admin-reset-password'),
    url(r'^admin/(?P<pk>\d+)/company/$',
        check_user_role(login_required(views.AccountCompanyListView.as_view())),
        name='admin-company-list'),

    # corporate
    url(r'^corporate/$',
        check_user_role(login_required(views.CompanyListView.as_view())),
        name='company-list'),
    url(r'^corporate/(?P<pk>\d+)/detail/$',
        check_corporate_permission(login_required(views.CompanyDetailView.as_view())),
        name='company-detail'),
    url(r'^corporate/(?P<pk>\d+)/update/$',
        check_corporate_permission(login_required(views.CompanyUpdateView.as_view())),
        name='company-update'),
    url(r'^corporate/(?P<pk>\d+)/update_status/$', 'tiger_admin.views.update_company_status', name='company-update-status'),
    url(r'^corporate/(?P<pk>\d+)/delete/$',
        check_corporate_permission(login_required(views.CompanyDeleteView.as_view())),
        name='company-delete'),
    url(r'^corporate/add/$',
        check_corporate_permission(login_required(views.CompanyCreateView.as_view())),
        name='company-add'),
    url(r'^corporate/(?P<pk>\d+)/product/$',
        check_corporate_permission(login_required(views.CompanyProductListView.as_view())),
        name='company-product-list'),
    url(r'^corporate/(?P<pk>\d+)/message/$', check_corporate_permission(login_required(views.CompanyMessageListView.as_view())),
        name='company-message-list'),

    # tag
    url(r'^category/$', login_required(views.CategoryListView.as_view()), name='category-list'),
    url(r'^category/add/$', login_required(views.CategoryCreateView.as_view()), name='category-add'),
    url(r'^category/(?P<pk>\d+)/detail/$', login_required(views.CategoryDetailView.as_view()), name='category-detail'),
    url(r'^category/(?P<pk>\d+)/update/$', login_required(views.CategoryUpdateView.as_view()), name='category-update'),
    url(r'^category/(?P<pk>\d+)/delete/$', login_required(views.CategoryDeleteView.as_view()), name='category-delete'),

    # product
    url(r'^product/$', login_required(views.ProductListView.as_view()), name='product-list'),
    url(r'^product/add/$', login_required(views.ProductCreateView.as_view()), name='product-add'),
    url(r'^product/(?P<pk>\d+)/detail/$', login_required(views.ProductDetailView.as_view()), name='product-detail'),
    url(r'^product/(?P<pk>\d+)/update/$', login_required(views.ProductUpdateView.as_view()), name='product-update'),
    url(r'^product/(?P<pk>\d+)/delete/$', login_required(views.ProductDeleteView.as_view()), name='product-delete'),

    # gallery
    url(r'^product/(?P<ppk>\d+)/gallery/$', login_required(views.ProductImageListView.as_view()), name='product-image-list'),
    url(r'^product/(?P<ppk>\d+)/gallery/add/$', login_required(views.GalleryCreateView.as_view()), name='gallery-add'),
    url(r'^product/(?P<ppk>\d+)/gallery/(?P<pk>\d+)/detail/$', login_required(views.GalleryDetailView.as_view()), name='gallery-detail'),
    url(r'^product/(?P<ppk>\d+)/gallery/(?P<pk>\d+)/delete/$', login_required(views.GalleryDeleteView.as_view()), name='gallery-delete'),
    url(r'^product/(?P<ppk>\d+)/gallery/(?P<pk>\d+)/update/$', login_required(views.GalleryUpdateView.as_view()), name='gallery-update'),

    # message
    url(r'^message/$', login_required(views.MessageListView.as_view()), name='message-list'),
    url(r'^message/(?P<pk>\d+)/detail/$', login_required(views.MessageDetailView.as_view()), name='message-detail'),
)
