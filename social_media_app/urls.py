"""
URL configuration for social_media_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.urls import include, path

from user import views as user_views
from post import views as post_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', post_views.home, name='home'),
    path('register/', user_views.user_register, name='register'),
    path('login/', user_views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='post/home.html'), name='logout'),

    path('user/', include('user.urls')),
    path('post/', include('post.urls')),
    path('friend/', include('friend.urls')),

    path('<str:username>/', user_views.profile, name='profile'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)