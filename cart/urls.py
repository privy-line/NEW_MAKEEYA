from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'cart'

urlpatterns=[
    url(r'cart', views.cart_detail, name='cart_detail'),
    url(r'^add/(d+)/$', views.cart_add, name='cart_add'),
    url(r'^remove/(d+)/$', views.cart_remove, name='cart_remove'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)