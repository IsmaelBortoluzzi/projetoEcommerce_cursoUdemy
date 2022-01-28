from django.template import Library
from utils import utils

register = Library()


@register.filter
def formata_preco(preco):
    return utils.formata_preco(preco)


@register.filter
def formata_str_preco(preco):
    return utils.formata_str_preco(preco)


@register.filter
def cart_total_qtd(carrinho):
    return utils.cart_total_qtd(carrinho)


@register.filter
def cart_totals(carrinho):
    return utils.cart_totals(carrinho)
