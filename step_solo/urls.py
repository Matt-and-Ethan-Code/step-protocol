from django.urls import URLPattern, URLResolver, path
import step_solo.views as views


urlpatterns: list[URLPattern | URLResolver] = [
    path('', views.index, name='step_solo_index'),
    path('what-to-expect', views.what_to_expect, name='solo_what_to_expect'),
    path('self-regulation-strategies', views.self_regulation_strategies, name='solo_self_regulation_strategies'),
    path('introduction', views.step_solo_introduction, name='solo_introduction')
]
