from django.urls import URLPattern, path
import provider_intake.views as views

urlpatterns: list[URLPattern] = [
    path('provider-intake/', views.provider_intake, name='provider_intake')
]