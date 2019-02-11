from django.conf.urls import url,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'index/$', views.Index, name="index"),
    url(r'object/$', views.Object, name="object"),
    url(r'^$', views.Index, name="index"),
    url(r'login/$', views.login, name="login"),
    url(r'into/$', views.into, name="into"),
    url(r'create/$', views.Create, name="create"),
    url(r'upload/$', views.upload, name="upload"),
    url(r'download/$', views.download, name="download"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)