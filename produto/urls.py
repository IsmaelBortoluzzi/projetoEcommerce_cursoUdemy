from django.urls import path
from . import views

app_name = 'produto'

urlpatterns = [
    path('', views.ListaProdutos.as_view(), name='lista'),
    path('<slug>', views.DetalheProduto.as_view(), name='detalhe'),
    path('addcarrinho/', views.AddCarrinhoProdutos.as_view(), name='add'),
    path('removecarrinho', views.RemoveCarrinhoProdutos.as_view(), name='remove'),
    path('carrinho/', views.CarrinhoProduto.as_view(), name='carrinho'),
    path('finalizar/', views.FinalizarProduto.as_view(), name='finalizar')
]