from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from transactions.views import HomePage

urlpatterns = [
    path('', HomePage.as_view()),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('transactions/', include('transactions.urls')),
    path('accounts/', include('accounts.urls')),
    path('captcha/', include('captcha.urls')),
    path('profile/', include('profiles.urls')),
]


handler404 = "app.views.page_not_found_view"

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
