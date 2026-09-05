"""
URL configuration for portofolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.http import HttpResponse

def test_view(request):
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Server Django</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 50px; }
            .success { color: green; }
            .info { color: blue; }
        </style>
    </head>
    <body>
        <h1 class="success">✅ Server Django Berjalan!</h1>
        <p class="info">Jika Anda melihat halaman ini, server Django sudah berjalan dengan baik.</p>
        <p>Waktu: <span id="time"></span></p>
        <p>URL: <strong>http://127.0.0.1:8000</strong> (bukan https)</p>
        <script>
            document.getElementById('time').textContent = new Date().toLocaleString();
        </script>
    </body>
    </html>
    """)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', test_view, name='test'),
    path('custom-admin/', include('custom_admin.urls')),
    path('', include('main_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
