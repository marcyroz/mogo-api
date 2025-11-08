from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("usuarios/", include("usuarios.urls")),
    path("social/", include("social.urls")),
    path("navigation/", include("navigation.urls")),
    ## path('analysis/', include('analysis.urls')),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
