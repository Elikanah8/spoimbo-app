from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views
from django.contrib.auth import views as auth_views # Import built-in auth views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Main Player
    path('', views.home, name='home'),
    
    # Payment Logic
    path('pay/<int:amount>/', views.initiate_mpesa, name='pay'),
    
    # Login and Logout (The missing link!)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('pay/<int:amount>/', views.initiate_mpesa, name='pay'),
    
    # Auth paths
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # NEW SIGNUP PATH
    path('signup/', views.signup, name='signup'), 
    path('favorite/<int:song_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('library/', views.my_library, name='library'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)