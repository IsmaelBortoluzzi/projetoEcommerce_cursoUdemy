from django.contrib import admin
from . import models


class VariacaoInLine(admin.TabularInline):
    model = models.Variacao
    extra = 1


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao_curta', 'get_formatted_price']
    inlines = [
        VariacaoInLine
    ]


admin.site.register(models.Produto, ProdutoAdmin)
admin.site.register(models.Variacao)
