from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

def redirect_to_control(request):
    return redirect('/control/')

urlpatterns = [
    path('admin/', redirect_to_control),
    path('control/', include('agency_admin.urls', namespace='agency_admin')),
    path('', include('public.urls', namespace='public')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
