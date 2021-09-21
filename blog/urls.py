from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    path('post/<int:pk>', views.post_detail, name='post_detail'),
    url(r'^post/create/$', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^login/$', views.user_login, name='login'),
]
