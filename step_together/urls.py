from django.urls import URLPattern, path
import step_together.views as views

urlpatterns: list[URLPattern] = [
    path('agreement/', views.agreement_view, name='agreement'), 
    path('step-together/', views.step_together_portal_view, name='step-together'),
    path('step-together/manual/', views.step_together_manual, name='step-together-manual')
]
