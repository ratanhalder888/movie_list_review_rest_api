from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('watch/', include("watchlist_app.api.urls")),
    path('account/',include("user_app.api.urls")),
    
    # path('api-auth', include('rest_framework.urls')),
] + debug_toolbar_urls()
