from django.urls import URLPattern, path
import step_together.views as views

urlpatterns: list[URLPattern] = [
    path('agreement/', views.agreement_view, name='agreement'), 
    path('step-together/', views.step_together_portal_view, name='step-together'),
    path('step-together/manual/', views.step_together_manual, name='step-together-manual'), 
    path('step-together/pregroup-checklist/', views.step_together_pregroup_checklist, name='step-together-pregroup-checklist'),
    path('step-together/welcome-to-step-together/', views.welcome_to_step_together, name='welcome-to-step-together'),
    path('step-together/self-care-introduction/', views.self_care_introduction, name='self-care-introduction'), 
    path('step-together/bilateral-tapping/', views.bilateral_tapping, name='bilateral-tapping'), 
    path('step-together/4-elements/', views.four_elements_pt1, name='four-elements'), 
    path('step-together/check-in/', views.check_in, name='check-in'), 
    path('step-together/protocol-sheet/', views.step_together_protocol_sheet, name='protocol-sheet'), 
    path('step-together/check-in-pt-2', views.check_in2, name='check-in-pt-2'), 
    path('step-together/container', views.container, name='container'), 
    path('step-together/4-elements-pt-2', views.four_elements_pt2, name='four-elements-part-2'), 
    path('step-together/ending', views.ending, name='ending'),
    path('step-together/post-group-checklist', views.post_group_checklist, name='post-group-checklist')
]
