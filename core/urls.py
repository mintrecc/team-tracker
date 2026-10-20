from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from workers.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("tasks.urls", namespace="tasks")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("/workers/", include("workers.urls", namespace="workers"))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
