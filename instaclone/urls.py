from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    url(r'detail/(\d+)/$', views.detail, name='detail'),
    url(r'^cart_detail/$', views.cart_detail, name='cart_detail'),
    url(r'^$',views.home,name='home'),  
    url(r'^upload/$', views.create_item, name='create_item'),
    url(r'^edit_profile',views.edit_profile, name='edit_profile'),
    url(r'^profile', views.profile, name='profile'), 
    url(r'^comments/(\d+)',views.comments,name="comments"),
    url(r'^buyer_registration/',views.buyer_registration,name='buyer_registration'),
    url(r'^buyer_login/',views.buyer_login,name='buyer_login'),
    url(r'^request/$', views.post_request, name='post_request'),
    url(r'^cart_add/(\d+)/$', views.cart_add, name='cart_add'),
    url(r'^remove/(\d+)/$', views.cart_remove, name='cart_remove'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)