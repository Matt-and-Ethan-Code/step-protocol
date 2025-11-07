from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_testing, name='start_testing'),
    path('questionnaire/<int:questionnaire_id>', views.questionnaire_view, name='questionnaire_view'),
    path('complete/', views.testing_complete, name='testing_complete')
]