from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    path('', views.PagarPedido.as_view(), name='pagar'),
    path('fecharpedido/', views.FecharPedido.as_view(), name='fechar'),
    path('detalhe/', views.DetalhePedido.as_view(), name='detalhe'),
]
