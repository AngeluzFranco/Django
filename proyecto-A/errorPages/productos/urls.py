from django.urls import path, include
from .views import *

urlpatterns = [
    path('api/get/', lista_productos, name='lista'),
    path('agregar/', agregar_producto, name='agregar'),
]