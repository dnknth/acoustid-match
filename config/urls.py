from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles import views as static_views
from django.urls import include, path
from django.views.generic.base import RedirectView


urlpatterns = [
    path( 'accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path( '__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns + [
        path( 'admin/doc/', include( 'django.contrib.admindocs.urls')),
        path( 'admin/', admin.site.urls),
        path( 'media/(<str:path>', static_views.serve,
            { 'document_root' : settings.MEDIA_ROOT }),
        path( '', RedirectView.as_view( url='/admin/')),
    ]
