from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('healthz', views.healthz, name='healthz'),
    path('api/layers/inundacion', views.flood_layer, name='flood_layer'),
    path('api/layers/vulnerabilidad', views.vulnerability_layer, name='vulnerability_layer'),
]