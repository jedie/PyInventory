from django.conf import settings
from django.conf.urls import include, static, url
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView


admin.autodiscover()

urlpatterns = [  # Don't use i18n_patterns() here
    path('admin/', admin.site.urls),

    url(r'^$', RedirectView.as_view(pattern_name='admin:index')),

    path('ckeditor/', include('ckeditor_uploader.urls')),  # TODO: check permissions?
    path(settings.MEDIA_URL.lstrip('/'), include('django_tools.serve_media_app.urls')),
]


if settings.SERVE_FILES:
    urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls))] + urlpatterns
