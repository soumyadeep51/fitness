from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict_workout, name='predict'),
    path('about/', views.about, name='about'),
    path('feedback/', views.feedback, name='feedback'),
    path('contact/', views.contact, name='contact'),
    path('register/',views.register,name='register'),
    path('login/',views.login_view,name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
