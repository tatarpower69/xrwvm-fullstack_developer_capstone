from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf.urls.static import static
from django.conf import settings

spa = ensure_csrf_cookie(TemplateView.as_view(template_name='index.html'))
urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),
    path('about/', TemplateView.as_view(template_name='About.html')),
    path('contact/', TemplateView.as_view(template_name='Contact.html')),
    re_path(r'^(?:|dealers/?|login/?|register/?|dealer/\d+/?|postreview/\d+/?)$', spa),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
