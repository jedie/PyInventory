from django.conf import settings
from django.conf.urls import include, static, url
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView


admin.autodiscover()

urlpatterns = [  # Don't use i18n_patterns() here
    path('admin/', admin.site.urls),

    url(r'^$', RedirectView.as_view(url='/admin/')),

    path('ckeditor/', include('ckeditor_uploader.urls')),  # TODO: check permissions?
]

if settings.DEBUG:
    urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar

    urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls))] + urlpatterns
