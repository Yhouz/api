from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # 🔥 Isso é obrigatório

    # Rotas do DRF-Spectacular
    # Rota para baixar o arquivo schema.yml da sua API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Rotas da UI do Swagger e Redoc:
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
