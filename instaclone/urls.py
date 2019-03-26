
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    url(r'^$',views.home,name='home'),  
    url(r'^upload/$', views.upload_image, name='upload_image'),
    url(r'^accounts/edit',views.edit_profile, name='edit_profile'),
    url(r'^profile', views.profile, name='profile'),  
    
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)