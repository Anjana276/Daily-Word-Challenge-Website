from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # Login page
    path('accounts/login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),

    # Django's built-in auth URLs (logout, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),

    # Root path → redirect to login
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),

    # Core app (register/signup)
    path('', include('core.urls')),

    # Words app (daily word page)
    path('', include('words.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
