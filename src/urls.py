
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions                                                                                                                                                                             
from django.conf import settings
from django.conf.urls.static import static

schema_view2 = get_schema_view(
    openapi.Info(
        title="KRATOS chatbot API",
        default_version='v1',
        description="KRATOS chatbot API",
        contact=openapi.Contact(email="info@chatbot.com"),

    ),
    public=True,
    permission_classes=(permissions.AllowAny,),

)

urlpatterns = [
    path('chatbot/api/', schema_view2.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('chatbot/api/admin/', admin.site.urls),
    path('chatbot/api/doc/swagger/', schema_view2.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('chatbot/api/v1/chat/', include('apps.chatbot.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
