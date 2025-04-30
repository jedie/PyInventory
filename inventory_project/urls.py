from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView


admin.autodiscover()

urlpatterns = [  # Don't use i18n_patterns() here
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='admin:index')),
    path('tinymce/', include('tinymce.urls')),  # TODO: check permissions?
    path(settings.MEDIA_URL.lstrip('/'), include('django_tools.serve_media_app.urls')),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
