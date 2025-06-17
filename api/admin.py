from django.contrib import admin

from api.models import Cardapio, Fornecedor, Funcionario, Usuario, Produto

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Funcionario)
admin.site.register(Produto)
admin.site.register(Fornecedor)
admin.site.register(Cardapio)