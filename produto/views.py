from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from . import models
from django.views.generic.detail import DetailView


class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 10


class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'


class AddCarrinhoProdutos(View):
    pass


class RemoveCarrinhoProdutos(View):
    pass


class CarrinhoProduto(View):
    pass


class FinalizarProduto(View):
    pass
