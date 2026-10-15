from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
import os
admin_path=os.getenv('DJANGO_ADMIN_URL','secure-admin/').strip('/')+'/'
urlpatterns=[path(admin_path,admin.site.urls),path('',include('website.urls'))]
if settings.DEBUG: urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
