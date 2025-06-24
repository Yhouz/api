from django.urls import path
from .views import (
    api_login, api_cadastro, buscar_cardapio,
    buscar_produto, cadastrar_cardapio, deletar_cardapio, deletar_produto, editar_cardapio, editar_produto, cadastro_produto,
    cadastro_funcionario, login_funcionario,
    listar_fornecedores, criar_fornecedor, detalhar_fornecedor,
    editar_fornecedor, deletar_fornecedor,recuperar_senha,carrinho_list_create, carrinho_detail,
    adicionar_item_carrinho, item_carrinho_detail
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView # Certifique-se de importar TokenBlacklistView se for usar para logout
)


urlpatterns = [
    path('login/', api_login, name='api_login'),
    path('cadastro/', api_cadastro, name='api_cadastro'),
    path('login-funcionario/', login_funcionario, name='login_funcionario'),
    path('cadastro-funcionario/', cadastro_funcionario, name='cadastro_funcionario'),
    path('recuperar-senha/', recuperar_senha, name='recuperar_senha'),
    
    # Produtos
    path('produtos/cadastrar/', cadastro_produto),
    path('produtos/', buscar_produto),
    path('produtos/<int:id>/', buscar_produto),
    path('produtos/editar/<int:id>/', editar_produto),
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

    # Carrinho de Compras
    path('carrinhos/', carrinho_list_create, name='carrinho_list_create'),
    path('carrinhos/<int:pk>/', carrinho_detail, name='carrinho_detail'),
    
    # ✅ CORREÇÃO AQUI: Adicione esta nova rota para adicionar itens ao carrinho
    path('carrinhos/<int:carrinho_id>/itens/', adicionar_item_carrinho, name='adicionar_item_carrinho_nested'),
    
    # Mantenha esta rota antiga se o frontend ainda a usar em algum lugar, mas a nova é preferível
    path('itens_carrinho/', adicionar_item_carrinho, name='adicionar_item_carrinho_flat'), 
    
    path('itens_carrinho/<int:pk>/', item_carrinho_detail, name='item_carrinho_detail'),

    # JWT Token Endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'), # Se você for usar para logout
]
