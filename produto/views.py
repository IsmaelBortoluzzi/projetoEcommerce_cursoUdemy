from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View


class ListaProdutos(ListView):
    pass


class DetalheProduto(View):
    pass


class AddCarrinhoProdutos(View):
    pass


class RemoveCarrinhoProdutos(View):
    pass


class CarrinhoProduto(View):
    pass


class FinalizarProduto(View):
    pass
