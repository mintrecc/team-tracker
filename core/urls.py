from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from tasks.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("tasks.urls", namespace="tasks")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", RegisterView.as_view(), name="register"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
