from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from produto.models import Variacao
from utils import utils
from pedido.models import Pedido, ItemPedido


class DispatchLoginRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


class PagarPedido(DispatchLoginRequiredMixin, DetailView):
    template_name = 'pedido/pagar.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'


class SalvarPedido(View):
    template_name = 'pedido/pagar.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Você não está logado'
            )
            return redirect('perfil:criar')

        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Carrinho vazio.'
            )
            return redirect('produto:lista')

        carrinho = self.request.session.get('carrinho')
        carrinho_variacao_ids = [variacao for variacao in carrinho]
        db_variacoes = list(
            Variacao.objects.select_related('produto').filter(id__in=carrinho_variacao_ids)
        )

        for variacao in db_variacoes:
            vid = str(variacao.id)

            error_msg_estoque = ''

            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unt = carrinho[vid]['preco_unitario']
            preco_unt_promo = carrinho[vid]['preco_unitario_promocional']

            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_quantidade'] = estoque * preco_unt
                carrinho[vid]['preco_quantidade_promocional'] = estoque * preco_unt_promo

                error_msg_estoque = 'Estoque insuficiente para alguns produtos do seu carrinho. ' \
                                    'Reduzimos a quantidade de produtos no seu carrinho. ' \
                                    'Verifique no carrinho quais produtos foram afetados.'

            if error_msg_estoque:
                messages.error(
                    self.request,
                    error_msg_estoque
                )
                self.request.session.save()
                return redirect('produto:carrinho')

        qtd_total_carrinho = utils.cart_total_qtd(carrinho)
        valor_total_carrinho = utils.cart_totals(carrinho)

        pedido = Pedido(
            user=self.request.user,
            total=valor_total_carrinho,
            qtd_total=qtd_total_carrinho,
            status='C'
        )

        pedido.save()

        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto=variacao['produto_nome'],
                    produto_id=variacao['produto_id'],
                    variacao=variacao['variacao_nome'],
                    variacao_id=variacao['variacao_id'],
                    preco=variacao['preco_quantitativo'],
                    preco_promocional=variacao['preco_quantitativo_promocional'],
                    quantidade=variacao['quantidade'],
                    imagem=variacao['imagem'],

                ) for variacao in carrinho.values()
            ]
        )

        contexto = {}

        del self.request.session['carrinho']
        # return render(self.request, self.template_name, contexto)
        return redirect(
            reverse(
                'pedido:pagar',
                kwargs={
                    'pk': pedido.pk
                }
            )
        )


class DetalhePedido(DispatchLoginRequiredMixin, DetailView):
    model = Pedido
    context_object_name = 'pedido'
    template_name = 'pedido/detalhe.html'
    pk_url_kwarg = 'pk'


class Lista(DispatchLoginRequiredMixin, ListView):
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedido/lista.html'
    paginate_by = 5
    ordering = ['-id']
