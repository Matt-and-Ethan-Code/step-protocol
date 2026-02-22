from django.urls import path
import authentication.views as views

urlpatterns = [
    path('session_expired', views.session_expired, name="session_expired")
]