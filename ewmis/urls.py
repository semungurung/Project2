"""ewmis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from user.views import login,Logout,signup_client, signup_vendor
from django_email_verification import urls as email_urls

urlpatterns = [
    path('', views.IndexPage.as_view(), name='index'),
    path('email/', include(email_urls)),
    path('dashboard/', include('ewmis.dash_urls')),
    path('login/', login, name='login'),
    path('logout/', Logout, name='logout'),
    path('signup/', signup_client, name='signup_client'),
    path('signup-vendor/', signup_vendor, name='signup_vendor'),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Error Pages
# handler400 = 'grisk_aware.core.views.handler400'
# handler403 = 'grisk_aware.core.views.handler403'
# handler404 = 'grisk_aware.core.views.handler404'
# handler500 = 'grisk_aware.core.views.handler500'


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

