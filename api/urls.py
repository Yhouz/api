from django.urls import path
from .views import (
    api_login, api_cadastro, buscar_cardapio,
    buscar_produto, cadastrar_cardapio, deletar_cardapio, deletar_produto, editar_cardapio, editar_produto, cadastro_produto,
    cadastro_funcionario, login_funcionario,
    listar_fornecedores, criar_fornecedor, detalhar_fornecedor,
    editar_fornecedor, deletar_fornecedor,
)

urlpatterns = [
    path('login/', api_login, name='api_login'),
    path('cadastro/', api_cadastro, name='api_cadastro'),
    path('login-funcionario/', login_funcionario, name='login_funcionario'),
    path('cadastro-funcionario/', cadastro_funcionario, name='cadastro_funcionario'),
    
    # Produtos
    path('produtos/cadastrar/', cadastro_produto),
    path('produtos/', buscar_produto),            # GET todos
    path('produtos/<int:id>/', buscar_produto),   # GET por ID
    path('produtos/editar/<int:id>/', editar_produto),  # PUT ou PATCH
    path('produtos/deletar/<int:id>/',deletar_produto),
    
    # Fornecedores
    path('fornecedores/', listar_fornecedores, name='listar_fornecedores'),
    path('fornecedores/criar/', criar_fornecedor, name='criar_fornecedor'),
    path('fornecedores/<int:id>/', detalhar_fornecedor, name='detalhar_fornecedor'),
    path('fornecedores/<int:id>/editar/', editar_fornecedor, name='editar_fornecedor'),
    path('fornecedores/<int:id>/deletar/', deletar_fornecedor, name='deletar_fornecedor'),

    # Cardapios 
    path('cardapios/', buscar_cardapio, name='listar_cardapios'),
    path('cardapios/<int:id>/', buscar_cardapio, name='detalhar_cardapio'),
    path('cardapios/cadastrar/', cadastrar_cardapio, name='cadastrar_cardapio'),
    path('cardapios/<int:id>/editar/', editar_cardapio, name='editar_cardapio'),
    path('cardapios/<int:id>/deletar/', deletar_cardapio, name='deletar_cardapio'),
]
