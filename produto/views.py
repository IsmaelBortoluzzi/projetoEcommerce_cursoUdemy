from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views import View
from . import models
from django.views.generic.detail import DetailView
from pprint import pprint


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
    def get(self, *args, **kwargs):
        # if self.request.session.get('carrinho'):
        #     del self.request.session['carrinho']
        #     self.request.session.save()

        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )  # redirect para a url que o user estava antes

        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(self.request, 'Produto não encontrado')
            return redirect(http_referer)

        variacao = get_object_or_404(models.Variacao, id=variacao_id)
        variacao_estoque = variacao.estoque
        produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        preco_unitario = produto.preco_marketing
        preco_unitario_promocional = produto.preco_marketing_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        if variacao_estoque < 1:
            messages.error(
                self.request,
                'Estoque insuficiente'
            )
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}  # cria essa chave na sessão do user
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x no produto "{produto_nome}".'
                    f'Adicionamos {variacao_estoque}x no seu carrinho.'
                )
                quantidade_carrinho = quantidade_carrinho

            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * quantidade_carrinho

        else:
            carrinho[variacao_id] = {
                    'produto_id': produto_id,
                    'produto_nome': produto_nome,
                    'variacao_nome': variacao_nome,
                    'variacao_id': variacao_id,
                    'preco_unitario': preco_unitario,
                    'preco_unitario_promocional': preco_unitario_promocional,
                    'quantidade': quantidade,
                    'preco_quantitativo':  preco_unitario,
                    'preco_quantitativo_promocional': preco_unitario_promocional,
                    'slug': slug,
                    'imagem': imagem,
            }

        self.request.session.save()
        messages.success(
            self.request,
            'Produto adicionado com sucesso!'
        )
        return redirect(http_referer)


class RemoveCarrinhoProdutos(View):
    pass


class CarrinhoProduto(View):

    def get(self, *args, **kwargs):
        contexto = {
            'carrinho': self.request.session.get('carrinho')
        }

        if not contexto['carrinho']:
            contexto['carrinho'] = {}

        return render(self.request, 'produto/carrinho.html', contexto)  # p 3 arg de render é o context


class FinalizarProduto(View):
    pass
