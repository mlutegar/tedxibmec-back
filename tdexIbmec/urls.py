from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from tdexIbmec.settings import BASE_DIR

schema_view = get_schema_view(
    openapi.Info(
        title="API TEDX",
        default_version='v1',
        description="Descrição da API",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contato@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url='https://tedxibmec.fly.dev/',
    # url='http://127.0.0.1:8000/',
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("backend.urls")),
    path('', include("frontend.urls")),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]

# no DEBUG ou usando WhiteNoise, mapeia /imagens/ para a pasta build/imagens
urlpatterns += static(
    '/imagens/',
    document_root=BASE_DIR / 'frontend' / 'build' / 'imagens'
)