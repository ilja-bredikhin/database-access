from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('thermometers.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # Маршрут для входа
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  # Маршрут для выхода
]