from django.conf.urls import patterns, include, url

from tiger_admin import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

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
    url(r'^admin/(?P<pk>\d+)/detail/$', views.AccountDetailView.as_view(), name='admin-detail'),
    url(r'^admin/(?P<pk>\d+)/update_status/$', 'tiger_admin.views.update_status', name='admin-update-status'),
    url(r'^admin/(?P<pk>\d+)/delete/$', views.AccountDeleteView.as_view(), name='admin-delete'),
    url(r'^admin/(?P<pk>\d+)/password_change/$', views.AccountPasswordResetView.as_view(), name='admin-change-password'),
    url(r'^admin/(?P<pk>\d+)/password_reset/$', 'tiger_admin.views.password_reset', name='admin-reset-password'),
    url(r'^admin/(?P<pk>\d+)/company/$', views.AccountCompanyListView.as_view(), name='admin-company-list'),

    # corporate
    url(r'^corporate/$', views.CompanyListView.as_view(), name='company-list'),
    url(r'^corporate/(?P<pk>\d+)/detail/$', views.CompanyDetailView.as_view(), name='company-detail'),
    url(r'^corporate/(?P<pk>\d+)/update/$', views.CompanyUpdateView.as_view(), name='company-update'),
    url(r'^corporate/(?P<pk>\d+)/update_status/$', 'tiger_admin.views.update_company_status', name='company-update-status'),
    url(r'^corporate/(?P<pk>\d+)/delete/$', views.CompanyDeleteView.as_view(), name='company-delete'),
    url(r'^corporate/add/$', views.CompanyCreateView.as_view(), name='company-add'),
    url(r'^corporate/(?P<pk>\d+)/product/$', views.CompanyProductListView.as_view(), name='company-product-list'),
    url(r'^corporate/(?P<pk>\d+)/video/$', views.CompanyVideoListView.as_view(), name='company-video-list'),

    # tag
    url(r'^category/$', views.CategoryListView.as_view(), name='category-list'),
    url(r'^category/add/$', views.CategoryCreateView.as_view(), name='category-add'),
    url(r'^category/(?P<pk>\d+)/detail/$', views.CategoryDetailView.as_view(), name='category-detail'),
    url(r'^category/(?P<pk>\d+)/update/$', views.CategoryUpdateView.as_view(), name='category-update'),
    url(r'^category/(?P<pk>\d+)/delete/$', views.CategoryDeleteView.as_view(), name='category-delete'),

    # product
    url(r'^product/$', views.ProductListView.as_view(), name='product-list'),
    url(r'^product/add/$', views.ProductCreateView.as_view(), name='product-add'),
    url(r'^product/(?P<pk>\d+)/detail/$', views.ProductDetailView.as_view(), name='product-detail'),
    url(r'^product/(?P<pk>\d+)/update/$', views.ProductUpdateView.as_view(), name='product-update'),
    url(r'^product/(?P<pk>\d+)/delete/$', views.ProductDeleteView.as_view(), name='product-delete'),


    url(r'^product/(?P<pk>\d+)/image/$', views.ProductImageListView.as_view(), name='product-image-list'),

)
