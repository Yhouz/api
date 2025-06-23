from datetime import datetime


import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CardapioSerializer, CarrinhoSerializer, ItemCarrinhoSerializer, ProdutoSerializer, FornecedorSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes



from .models import Cardapio, Carrinho, Funcionario, ItemCarrinho, Usuario, Produto, Fornecedor




@api_view(['POST'])
def api_cadastro(request):
    nome = request.data.get('nome')
    senha = request.data.get('senha')
    tipo_usuario = request.data.get('tipo_usuario')
    email = request.data.get('email')  # noqa: F811
    telefone = request.data.get('telefone')
    cpf = request.data.get('cpf')

    # Validação dos campos obrigatórios
    #if not senha or not email:
    if not nome or not senha or not tipo_usuario or not email or not cpf:
        return Response({'success': False, 'message': 'Campos obrigatórios faltando.'}, status=400)

    # 🔥 Validação do e-mail institucional
    if not email.endswith('@unifucamp.edu.br'):
        return Response({'success': False, 'message': 'Use um e-mail institucional (@unifucamp.edu.br)'}, status=400)

    # Verificar se já existe usuário com mesmo nome, email ou CPF
    if Usuario.objects.filter(nome=nome).exists():
        return Response({'success': False, 'message': 'Nome de usuário já existe.'}, status=409)

    if Usuario.objects.filter(email=email).exists():
        return Response({'success': False, 'message': 'Email já cadastrado.'}, status=409)

    if Usuario.objects.filter(cpf=cpf).exists():
        return Response({'success': False, 'message': 'CPF já cadastrado.'}, status=409)

    # Criptografar a senha
    usuario = Usuario(
        nome=nome,
        tipo_usuario=tipo_usuario,
        email=email,
        telefone=telefone,
        cpf=cpf,
        senha=senha
    )
    usuario.save()
  

    return Response({
        'success': True,
        'message': 'Usuário cadastrado com sucesso.',
        'usuario': {
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'cpf': usuario.cpf,
            'telefone': usuario.telefone,
            'tipo_usuario': usuario.tipo_usuario,
            'saldo_carteira': str(usuario.saldo_carteira),
            'data_cadastro': usuario.data_cadastro
        }
    })

@api_view(['POST'])
def api_login(request):
    email = request.data.get('email')
    senha = request.data.get('senha')
    tipo_usuario = request.data.get('tipo_usuario')

    if not email or not senha or not tipo_usuario:
        return Response({'success': False, 'message': 'email e senha tipo_usuario são obrigatórios.'}, status=400)

    try:

        usuario = Usuario.objects.get(email=email, tipo_usuario=tipo_usuario)
        if usuario.senha == senha:  # ⚠️ Sempre recomendo usar hash na senha
            return Response({
                'success': True,
                'usuario': {
                    'id': usuario.id,
                    'nome': usuario.nome,
                    'email': usuario.email,
                    'cpf': usuario.cpf,
                    'telefone': usuario.telefone,
                    'tipo_usuario': usuario.tipo_usuario,
                    'saldo_carteira': str(usuario.saldo_carteira),
                    'data_cadastro': usuario.data_cadastro
                }
            })
        else:
            return Response({'success': False, 'message': 'Senha incorreta.'}, status=401)
    except Usuario.DoesNotExist:
        return Response({'success': False, 'message': 'Usuário não encontrado.'}, status=404)
# FUNCIONARIO

@api_view(['POST'])
def cadastro_funcionario(request):
    nome = request.data.get('nome')
    senha = request.data.get('senha')
    email = request.data.get('email')
    telefone = request.data.get('telefone')
    cpf = request.data.get('cpf')
    cargo = request.data.get('cargo')
    dt_admissao = request.data.get('dt_admissao')
    dt_nascimento = request.data.get('dt_nascimento')
    salario = request.data.get('salario')
    endereco = request.data.get('endereco')
    numero = request.data.get('numero')  # Corrigido: 'numero' em vez de 'bairro'
    bairro = request.data.get('bairro')  # Corrigido: 'bairro' em vez de 'barrio'
    uf = request.data.get('uf')
    cidade = request.data.get('cidade')

    # Verificar campos obrigatórios
    if not nome or not senha or not email or not cpf or not cargo:
        return Response({'success': False, 'message': 'Campos obrigatórios faltando.'}, status=400)

    # Verificar se o usuário já existe
    if Usuario.objects.filter(nome=nome).exists():
        return Response({'success': False, 'message': f'Nome "{nome}" já cadastrado.'}, status=409)
    if Usuario.objects.filter(email=email).exists():
        return Response({'success': False, 'message': f'Email "{email}" já cadastrado.'}, status=409)
    if Usuario.objects.filter(cpf=cpf).exists():
        return Response({'success': False, 'message': f'CPF "{cpf}" já cadastrado.'}, status=409)


    
    # Criar o usuário
    usuario = Usuario(
        nome=nome,
        senha=senha,  # Sem criptografia!
        email=email,
        telefone=telefone,
        cpf=cpf,
        tipo_usuario='Funcionario'
    )
    usuario.save()

    # Criar o funcionário
    funcionario = Funcionario(
        usuario=usuario,
        cargo=cargo,
        dt_admissao=dt_admissao,
        dt_nascimento=dt_nascimento,
        salario=salario,
        endereco=endereco,
        numero=numero,
        bairro=bairro,
        uf=uf,
        cidade=cidade
    )
    funcionario.save()

    return Response({
        'success': True,
        'message': 'Funcionário cadastrado com sucesso.',
        'funcionario': {
            'id_funcionario': funcionario.id_funcionario,
            'nome': usuario.nome,
            'email': usuario.email,
            'cpf': usuario.cpf,
            'telefone': usuario.telefone,
            'cargo': funcionario.cargo,
            'tipo_usuario': usuario.tipo_usuario,
            'dt_admissao': funcionario.dt_admissao,
            'dt_nascimento': funcionario.dt_nascimento,
            'salario': funcionario.salario,
            'endereco': funcionario.endereco,
            'numero': funcionario.numero,
            'bairro': funcionario.bairro,
            'uf': funcionario.uf,
            'cidade': funcionario.cidade
        }
    })

@api_view(['POST'])
def login_funcionario(request):
    email = request.data.get('email')
    senha = request.data.get('senha')
    tipo_usuario = request.data.get('tipo_usuario')

    if not email or not senha:
        return Response({'success': False, 'message': 'Email e senha são obrigatórios.'}, status=400)

    try:
        usuario = Usuario.objects.get(nome=email, tipo_usuario=tipo_usuario)

        if senha == usuario.senha:  # Verificação direta sem hash
            funcionario = Funcionario.objects.get(usuario=usuario)
            return Response({
                'success': True,
                'funcionario': {
                    'id_funcionario': funcionario.id_funcionario,
                    'nome': usuario.nome,
                    'email': usuario.email,
                    'cpf': usuario.cpf,
                    'telefone': usuario.telefone,
                    'cargo': funcionario.cargo,
                    'data_cadastro': usuario.data_cadastro,
                    'tipo_usuario': usuario.tipo_usuario,
                    'dt_admissao': funcionario.dt_admissao,
                    'dt_nascimento': funcionario.dt_nascimento,
                    'salario': funcionario.salario,
                    'endereco': funcionario.endereco,
                    'numero': funcionario.numero,
                    'bairro': funcionario.bairro,
                    'uf': funcionario.uf,
                    'cidade': funcionario.cidade
                }
            })
        else:
            return Response({'success': False, 'message': 'Senha incorreta.'}, status=401)

    except Usuario.DoesNotExist:
        return Response({'success': False, 'message': 'Funcionário não encontrado.'}, status=404)

    except Funcionario.DoesNotExist:
        return Response({'success': False, 'message': 'Funcionário não cadastrado.'}, status=404)
    


@api_view(['POST'])
def cadastro_produto(request):
    nome = request.data.get('nome')
    descricao = request.data.get('descricao')
    preco = request.data.get('preco')
    quantidade_estoque = request.data.get('quantidade_estoque')
    categoria = request.data.get('categoria')
    custo = request.data.get('custo')
    margem = request.data.get('margem')
    unidade = request.data.get('unidade')
    imagem = request.FILES.get('imagem') # Ok, você pega a imagem aqui

    if not nome or not preco or not quantidade_estoque or not categoria:
        return Response({'success': False, 'message': 'Campos obrigatórios faltando.'}, status=400)

    # Verifica se já existe produto com o mesmo nome
    if Produto.objects.filter(nome=nome).exists():
        return Response({'success': False, 'message': 'Produto já cadastrado com esse nome.'}, status=409)

    # Cria o objeto Produto
    produto = Produto.objects.create(
        nome=nome,
        descricao=descricao,
        preco=preco,
        quantidade_estoque=quantidade_estoque,
        categoria=categoria,
        custo=custo,
        margem=margem,
        unidade=unidade
    )

    # ATRIBUI A IMAGEM AO CAMPO DO PRODUTO AQUI!
    if imagem: # Verifica se uma imagem foi enviada
        produto.imagem = imagem

    produto.save() # Agora, o campo 'imagem' será salvo junto com o resto

    return Response({
        'success': True,
        'message': 'Produto cadastrado com sucesso.',
        'produto': ProdutoSerializer(produto).data # Isso requer um Serializer
    }, status=201)


# 🔹 Buscar todos os produtos ou por ID
@api_view(['GET'])
def buscar_produto(request, id=None):
    if id:
        try:
            produto = Produto.objects.get(id=id)
            serializer = ProdutoSerializer(produto)
            return Response(serializer.data)
        except Produto.DoesNotExist:
            return Response({'success': False, 'message': 'Produto não encontrado.'}, status=404)
    else:
        produtos = Produto.objects.all()
        serializer = ProdutoSerializer(produtos, many=True)
        return Response(serializer.data)


# 🔹 Editar produto
@api_view(['PUT', 'PATCH'])
def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    serializer = ProdutoSerializer(produto, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': 'Produto atualizado com sucesso.',
            'produto': serializer.data
        })
    return Response({'success': False, 'errors': serializer.errors}, status=400)

@api_view(['DELETE'])
def deletar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    return Response({'success': True, 'message': 'Produto deletado com sucesso.'}, status=status.HTTP_204_NO_CONTENT)  # noqa: F821



@api_view(['GET'])
def listar_fornecedores(request):
    fornecedores = Fornecedor.objects.all()
    serializer = FornecedorSerializer(fornecedores, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def criar_fornecedor(request):
    serializer = FornecedorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'fornecedor': serializer.data}, status=201)
    return Response({'success': False, 'errors': serializer.errors}, status=400)


@api_view(['GET'])
def detalhar_fornecedor(request, id):
    fornecedor = get_object_or_404(Fornecedor, id=id)
    serializer = FornecedorSerializer(fornecedor)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
def editar_fornecedor(request, id):
    fornecedor = get_object_or_404(Fornecedor, id=id)
    serializer = FornecedorSerializer(fornecedor, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'fornecedor': serializer.data})
    return Response({'success': False, 'errors': serializer.errors}, status=400)


@api_view(['DELETE'])
def deletar_fornecedor(request, id):
    fornecedor = get_object_or_404(Fornecedor, id=id)
    fornecedor.delete()
    return Response({'success': True, 'message': 'Fornecedor deletado com sucesso.'})



# 🔹 Cadastrar novo cardápio
@api_view(["POST"])
def cadastrar_cardapio(request):
    nome = request.data.get("nome")
    categoria = request.data.get("categoria")
    data_str = request.data.get("data")
    produtos_str = request.data.get("produtos")

    # 1. Validação dos campos obrigatórios do Cardapio
    if not nome or not categoria or not data_str or not produtos_str:
        return Response(
            {"success": False, "message": "Campos obrigatórios (nome, categoria, data, produtos) faltando."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 2. Converter a string de data para objeto DateField
    try:
        data = datetime.strptime(data_str, "%Y-%m-%d").date() # Corrigido o formato da data
    except ValueError:
        return Response(
            {"success": False, "message": "Formato de data inválido. Use YYYY-MM-DD."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 3. Parsear a string JSON de produtos para uma lista de IDs
    try:
        produto_ids = json.loads(produtos_str)
        if not isinstance(produto_ids, list):
            raise ValueError("Produtos deve ser uma lista de IDs.")
    except (json.JSONDecodeError, ValueError) as e:
        return Response(
            {"success": False, "message": f"Formato de produtos inválido: {e}"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # ====================================================================
    # >>> AS LINHAS PRINT E A VERIFICAÇÃO DE PRODUTOS ESTÃO AGORA NO LUGAR CORRETO:
    print(f"IDs de produtos recebidos: {produto_ids}")
    existing_products = Produto.objects.filter(id__in=produto_ids)
    print(f"Produtos encontrados no DB: {[p.id for p in existing_products]}")

    # 4. Verificar se os produtos existem (AGORA SEM DUPLICAÇÃO E NA ORDEM CORRETA)
    if len(existing_products) != len(produto_ids):
        return Response(
            {"success": False, "message": "Um ou mais produtos não encontrados."},
            status=status.HTTP_400_BAD_REQUEST
        )
    # ====================================================================

    # 5. Lidar com a imagem (se presente)
    imagem = request.FILES.get("imagem")

    try:
        cardapio = Cardapio.objects.create(
            nome=nome,
            categoria=categoria,
            data=data,
            imagem=imagem # Atribui a imagem diretamente
        )
        cardapio.produtos.set(existing_products) # Define a relação ManyToMany
        cardapio.save()

        # Se você tiver um CardapioSerializer, use-o aqui:
        # serializer = CardapioSerializer(cardapio)
        # return Response({
        #     "success": True,
        #     "message": "Cardápio cadastrado com sucesso.",
        #     "cardapio": serializer.data
        # }, status=status.HTTP_201_CREATED)

        return Response(
            {"success": True, "message": "Cardápio cadastrado com sucesso."},
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response(
            {"success": False, "message": f"Erro interno ao criar cardápio: {e}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    
# 🔹 Buscar cardápio por ID ou listar todos

@api_view(['GET'])
def buscar_cardapio(request, id=None): # Keep 'id=None' if you want to keep the existing single ID route too
    # Check for 'ids' query parameter (e.g., /cardapios/?ids=20,19)
    ids_param = request.query_params.get('ids')

    if ids_param:
        try:
            # Convert comma-separated string of IDs to a list of integers
            list_of_ids = [int(id_str.strip()) for id_str in ids_param.split(',') if id_str.strip().isdigit()]
            
            if list_of_ids:
                # Filter Cardapios by the provided IDs
                cardapios = Cardapio.objects.filter(id__in=list_of_ids)
                serializer = CardapioSerializer(cardapios, many=True)
                return Response(serializer.data)
            else:
                return Response({'success': False, 'message': 'No valid IDs provided in the "ids" parameter.'}, status=400)
        except ValueError:
            return Response({'success': False, 'message': 'Invalid ID format. Use numbers separated by commas.'}, status=400)
    
    # If a specific ID was passed in the URL path (e.g., /cardapios/123/)
    elif id:
        try:
            cardapio = Cardapio.objects.get(id=id)
            serializer = CardapioSerializer(cardapio)
            return Response(serializer.data)
        except Cardapio.DoesNotExist:
            return Response({'success': False, 'message': 'Cardapio not found.'}, status=404)
    
    # If no 'ids' query parameter and no specific ID in the URL path, return all cardapios
    else:
        cardapios = Cardapio.objects.all()
        serializer = CardapioSerializer(cardapios, many=True)
        return Response(serializer.data)


# 🔹 Editar cardápio
@api_view(['PUT', 'PATCH'])
def editar_cardapio(request, id):
    cardapio = get_object_or_404(Cardapio, id=id)
    serializer = CardapioSerializer(cardapio, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': 'Cardápio atualizado com sucesso.',
            'cardapio': serializer.data
        })
    return Response({'success': False, 'errors': serializer.errors}, status=400)


# 🔹 Deletar cardápio
@api_view(['DELETE'])
def deletar_cardapio(request, id):
    cardapio = get_object_or_404(Cardapio, id=id)
    cardapio.delete()
    return Response({'success': True, 'message': 'Cardápio deletado com sucesso.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def recuperar_senha(request):
    print(f"Dados recebidos na requisição: {request.data}") # <-- ADICIONE ESTA LINHA AQUI
    email = request.data.get('email')
    nova_senha = request.data.get('nova_senha')

    if not email or not nova_senha:
        return Response({'success': False, 'message': 'Email e nova senha são obrigatórios.'}, status=400)

    # Adicionar validações de senha aqui (ex: comprimento mínimo)
   # if len(nova_senha) : # Exemplo de validação de comprimento
    #    return Response({'success': False, 'message': 'A nova senha deve ter no mínimo 8 caracteres.'}, status=400)
    # Adicione outras validações de complexidade conforme necessário

    try:
        usuario = Usuario.objects.get(email=email)

        # 🟢 CORREÇÃO CRÍTICA: Use make_password para hash a senha
        # antes de atribuir ao campo 'senha'
        usuario.senha = nova_senha
        usuario.save()

        return Response({'success': True, 'message': 'Senha atualizada com sucesso.'})
    except Usuario.DoesNotExist:
        return Response({'success': False, 'message': 'Usuário não encontrado.'}, status=404)
    except Exception as e:
        # Capture outras exceções para depuração
        print(f"Erro inesperado ao tentar recuperar senha: {e}")
        return Response({'success': False, 'message': 'Erro interno do servidor.'}, status=500)


# -------------------------------
# CARRINHO
# -------------------------------

@api_view(['GET', 'POST'])
#@permission_classes([IsAuthenticated])
def carrinho_list_create(request):
    if request.method == 'GET':
        # Filtrar só os carrinhos do usuário logado
        carrinhos = Carrinho.objects.filter(usuario=request.user)
        serializer = CarrinhoSerializer(carrinhos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Forçar que o carrinho seja criado para o usuário autenticado
        data = request.data.copy()
        data['usuario'] = request.user.id
        serializer = CarrinhoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
#@permission_classes([IsAuthenticated])
def carrinho_detail(request, pk):
    try:
        carrinho = Carrinho.objects.get(pk=pk)
    except Carrinho.DoesNotExist:
        return Response({'erro': 'Carrinho não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # Proteção: só o dono pode acessar
    if carrinho.usuario != request.user:
        return Response({'erro': 'Acesso negado. Você não é dono deste carrinho.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = CarrinhoSerializer(carrinho)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CarrinhoSerializer(carrinho, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        carrinho.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------------------
# ITEM DO CARRINHO
# -------------------------------

@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def adicionar_item_carrinho(request):
    carrinho_id = request.data.get('carrinho')
    if not carrinho_id:
        return Response({'erro': 'ID do carrinho é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        carrinho = Carrinho.objects.get(id=carrinho_id)
    except Carrinho.DoesNotExist:
        return Response({'erro': 'Carrinho não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # Proteção: só o dono pode adicionar itens ao próprio carrinho
    if carrinho.usuario != request.user:
        return Response({'erro': 'Você não tem permissão para adicionar itens neste carrinho.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = ItemCarrinhoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    print('Erro no serializer:', serializer.errors)
    print('Dados recebidos:', request.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT', 'DELETE'])
#@permission_classes([IsAuthenticated])
def item_carrinho_detail(request, pk):
    try:
        item = ItemCarrinho.objects.get(pk=pk)
    except ItemCarrinho.DoesNotExist:
        return Response({'erro': 'Item do carrinho não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # Proteção: só o dono do carrinho pode modificar o item
    if item.carrinho.usuario != request.user:
        return Response({'erro': 'Você não tem permissão para alterar este item.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = ItemCarrinhoSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
