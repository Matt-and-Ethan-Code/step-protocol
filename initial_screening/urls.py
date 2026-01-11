from django.urls import path
import initial_screening.views as views

urlpatterns = [
    path('', views.home_view, name="home_page"),
    path('start/', views.start_testing, name='start_testing'),
    path('questionnaire/<int:questionnaire_id>', views.questionnaire_view, name='questionnaire_view'),
    path('complete/', views.testing_complete, name='testing_complete'),
    path('itq-sample-response/', views.itq_email, name='itq_email'),
    path('dass21-sample-response/', views.dass21_email, name='dass21_email'),
    path('pcl5-sample-response/', views.pcl5_email, name='pcl5_email'),
]