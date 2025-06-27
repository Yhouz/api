from django.urls import path
from .views import (
    api_login, api_cadastro, buscar_cardapio,
    buscar_produto, cadastrar_cardapio, deletar_cardapio, deletar_produto, detalhar_pedido_finalizar, editar_cardapio, editar_produto, cadastro_produto,
    cadastro_funcionario, listar_produtos, login_funcionario,
    listar_fornecedores, criar_fornecedor, detalhar_fornecedor,
    editar_fornecedor, deletar_fornecedor,recuperar_senha,carrinho_list_create, carrinho_detail,
    adicionar_item_carrinho, item_carrinho_detail, meu_carrinho_aberto_detail,criar_pedido, listar_pedidos, detalhar_pedido,  deletar_pedido, finalizar_pedido
    ,finalizar_carrinho, meus_pedidos
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
    path('produtos/listar/',listar_produtos, name='listar_produtos_com_filtro'),
    
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
    path('cardapios/<str:data>/dia/', buscar_cardapio, name='buscar_cardapio_por_data'),

      # --- ROTAS DO CARRINHO DE COMPRAS ---
    path('carrinhos/', carrinho_list_create, name='carrinho-list-create'),
    
    # ✅ ROTA ESSENCIAL: Busca o carrinho ativo do usuário logado.
    # Deve vir ANTES da rota com <int:pk>.
    path('carrinhos/meu-carrinho/', meu_carrinho_aberto_detail, name='meu-carrinho-detail'),

    path('carrinhos/<int:pk>/', carrinho_detail, name='carrinho-detail-by-pk'),
    path('carrinhos/<int:carrinho_id>/finalizar/', finalizar_carrinho, name='finalizar-carrinho'),

    # --- ROTAS DOS ITENS DO CARRINHO ---
    path('carrinhos/<int:carrinho_id>/itens/', adicionar_item_carrinho, name='adicionar-item'),
    
    path('itens_carrinho/<int:pk>/', item_carrinho_detail, name='item-detail'),

    # JWT Token Endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'), # Se você for usar para logout

    # Pedido
    path('pedidos/', listar_pedidos, name='listar_pedidos'),
    path('pedidos/usuario/<int:id>', listar_pedidos, name='listar_pedidos'),
    path('pedidos/<int:id>/', detalhar_pedido, name='detalhar_pedido'),
    path('pedidos/criar/', criar_pedido, name='criar_pedido'),  
    path('pedidos/<int:id>/deletar/', deletar_pedido, name='deletar_pedido'),
    path('pedidos/<int:id>/finalizar/', finalizar_pedido, name='finalizar_pedido'),
    path('pedidos/meus-pedidos/', meus_pedidos, name='meus-pedidos'),
    path('pedidos/<int:id>/detalhar/', detalhar_pedido_finalizar, name='detalhar_pedido_finalizar'),
  
    
]
