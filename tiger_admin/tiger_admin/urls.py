from django.conf.urls import patterns, include, url

from tiger_admin import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tiger_admin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'tiger_admin.views.home', name='home'),
    url(r'^login/$', 'tiger_admin.views.login', name='login'),
    url(r'^logout/$', 'tiger_admin.views.logout', name='logout'),
    url(r'^admin/$', 'tiger_admin.views.admin_list', name='admin-list'),
    url(r'^admin/add/$', 'tiger_admin.views.admin_add', name='admin-add'),
    url(r'^admin/(?P<pk>\d+)/detail/$', views.AccountDetailView.as_view(), name='admin-detail'),
    url(r'^admin/(?P<pk>\d+)/update/$', views.AccountUpdateView.as_view(), name='admin-update'),
    url(r'^admin/(?P<pk>\d+)/delete/$', views.AccountDeleteView.as_view(), name='admin-delete'),
    url(r'^admin/(?P<pk>\d+)/password_reset/$', views.AccountPasswordResetView.as_view(), name='admin-reset-password'),
    url(r'^admin/(?P<pk>\d+)/company/$', views.AccountCompanyListView.as_view(), name='admin-company-list'),

)
