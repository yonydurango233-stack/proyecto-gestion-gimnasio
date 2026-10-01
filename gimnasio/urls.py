from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('core.urls')),
    path('entradas/', include('entradas_diarias.urls')),
    path('ventas-planes/', include('ventas_planes.urls')),
    path('ventas-productos/', include('ventas_productos.urls')),
    path('egresos/', include('egresos.urls')),
    path('planes/', include('planes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)