from django.urls import URLPattern, URLResolver, path
import step_solo.views as views


urlpatterns: list[URLPattern | URLResolver] = [
    path('', views.index, name='solo_index'),
    path('what-to-expect', views.what_to_expect, name='solo_what_to_expect'),
    path('self-regulation-strategies', views.self_regulation_strategies, name='solo_self_regulation_strategies'),
    path('introduction', views.step_solo_introduction, name='solo_introduction'),
    path('getting_started', views.getting_started, name='solo_getting_started'),
    path('bilateral_tapping', views.bilateral_tapping, name='solo_bilateral_tapping'),
    path('pre_check_in', views.pre_check_in, name='solo_pre_check_in'),
]
