from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import RedirectView


admin.autodiscover()

urlpatterns = [  # Don't use i18n_patterns() here
    path('admin/', admin.site.urls),
    re_path(r'^$', RedirectView.as_view(pattern_name='admin:index')),
    path(settings.MEDIA_URL.lstrip('/'), include('django_tools.serve_media_app.urls')),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [re_path(r'^__debug__/', include(debug_toolbar.urls))] + urlpatterns
