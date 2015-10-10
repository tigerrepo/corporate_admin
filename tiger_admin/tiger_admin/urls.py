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
    url(r'^corporaten/$', views.CompanyListView.as_view(), name='company-list'),
    url(r'^corporaten/(?P<pk>\d+)/detail/$', views.CompanyListView.as_view(), name='company-detail'),
    url(r'^corporaten/add/$', views.CompanyCreateView.as_view(), name='company-add'),

)
