from rest_framework import serializers
from .models import Cardapio, Carrinho, ItemCarrinho, Usuario, Funcionario, Produto, Fornecedor, Pedido, PedidoItem


class UsuarioSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id', 'nome', 'email', 'senha', 'cpf', 'telefone',
            'tipo_usuario', 'saldo_carteira', 'data_cadastro'
        ]
        read_only_fields = ['id', 'data_cadastro']

    def validate_email(self, value):
        if not value.endswith('@unifucamp.edu.br'):
            raise serializers.ValidationError(
                'Use um e-mail institucional (@unifucamp.edu.br)'
            )
        return value

    def create(self, validated_data):
        return Usuario.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = ['id_funcionario', 'usuario', 'cargo', 'dt_admissao','dt_nascimento',
                  'salario','endereco', 'numero', 'bairro', 'uf','cidade']




class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'
        

    def validate_quantidadeEstoque(self, value): # <-- Procure por algo assim
        if value < 0:
            raise serializers.ValidationError("A quantidade em estoque não pode ser negativa.")
        return value


class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = '__all__'

class CardapioSerializer(serializers.ModelSerializer):
    # Este campo espera uma lista de IDs de produtos
    # A configuração default para ManyToManyField em serializers é ler/escrever IDs
    produtos = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Produto.objects.all(), 
        allow_empty=True # Permite que o cardápio seja criado sem produtos
    )

    class Meta:
        model = Cardapio
        fields = '__all__' # Ou especifique os campos que você quer incluir

    # O método create já deve lidar com a relação ManyToMany se o campo estiver configurado corretamente
    # no Serializer e no seu modelo Cardapio.
    # Se ainda estiver com problemas, você pode precisar sobrescrever o .create() aqui:
    # def create(self, validated_data):
    #     produtos_data = validated_data.pop('produtos', [])
    #     cardapio = Cardapio.objects.create(**validated_data)
    #     cardapio.produtos.set(produtos_data) # produtos_data já são os objetos Produto
    #     return cardapio

class ItemCarrinhoSerializer(serializers.ModelSerializer):
    # Para exibir os detalhes do produto, e não apenas o ID.
    # `read_only=True` significa que este campo é usado para exibir dados, não para receber.
    produto = ProdutoSerializer(read_only=True)
    
    # Para receber o ID do produto ao criar um novo item.
    # `write_only=True` significa que este campo é usado para receber dados, não para exibir.
    produto_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ItemCarrinho
        fields = [
            'id', 
            'carrinho', 
            'produto',       # Para exibir os detalhes do produto
            'produto_id',    # Para receber o ID do produto na criação
            'quantidade', 
            'subtotal'
        ]
        
        # ✅ ✅ ✅ A CORREÇÃO PRINCIPAL ESTÁ AQUI ✅ ✅ ✅
        # Ao declarar 'carrinho' como um campo de "apenas leitura" (read-only),
        # o serializer não vai mais exigi-lo no corpo da requisição de um PUT/PATCH.
        # Ele entenderá que o carrinho do item já existe e não deve ser alterado.
        read_only_fields = ['carrinho', 'subtotal']

    def validate_quantidade(self, value):
        """
        Validação de estoque diretamente no serializer.
        """
        # Ao criar (self.instance é None), ou ao atualizar (self.instance existe)
        produto = None
        if self.instance:
            # Atualização: pega o produto do item existente
            produto = self.instance.produto
        else:
            # Criação: pega o produto_id dos dados validados
            produto_id = self.initial_data.get('produto_id')
            if produto_id:
                produto = Produto.objects.get(pk=produto_id)

        if produto and value > produto.quantidade_estoque:
            raise serializers.ValidationError(f"Estoque insuficiente. Apenas {produto.quantidade_estoque} unidades disponíveis.")
        
        return value

    def create(self, validated_data):
        """
        Garante que o produto seja atribuído corretamente ao criar um novo item.
        """
        # `produto_id` foi validado, agora usamos para criar o item.
        validated_data['produto_id'] = validated_data.pop('produto_id')
        return super().create(validated_data)


    
class CarrinhoSerializer(serializers.ModelSerializer):
    itens = ItemCarrinhoSerializer(many=True, read_only=True)
    total_itens = serializers.SerializerMethodField()
    total_valor = serializers.SerializerMethodField()

    class Meta:
        model = Carrinho
        fields = ['id', 'usuario', 'criado_em', 'atualizado_em', 'finalizado', 'itens', 'total_itens', 'total_valor']
        # ✅ Certifique-se que 'usuario' está em read_only_fields aqui.
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'total_itens', 'total_valor', 'usuario']

    def get_total_itens(self, obj):
        return obj.total_itens()

    def get_total_valor(self, obj):
        return obj.total_valor()

    def create(self, validated_data):
        # ✅ Esta é a lógica que precisa do 'request' no contexto
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['usuario'] = request.user # Atribui o usuário autenticado
        else:
            # ❗ Essa parte é importante para depurar:
            # Se chegar aqui, significa que o request.user não estava disponível/autenticado no contexto
            raise serializers.ValidationError("Usuário autenticado não encontrado no contexto do serializer para criar o carrinho.")

        return super().create(validated_data)
    
class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemCarrinhoSerializer(many=True, read_only=True)
    total_itens = serializers.SerializerMethodField()
    total_valor = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = ['id', 'usuario', 'carrinho', 'data_pedido', 'status', 'itens', 'total_itens', 'total_valor']
        read_only_fields = ['id', 'data_pedido', 'status', 'itens', 'total_itens', 'total_valor']

    def get_total_itens(self, obj):
        return obj.carrinho.total_itens()

    def get_total_valor(self, obj):
        return obj.carrinho.total_valor()


class PedidoItemSerializer(serializers.ModelSerializer):
    produto = ProdutoSerializer(read_only=True)
    produto_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = PedidoItem
        fields = ['id', 'pedido', 'produto', 'produto_id', 'quantidade']
        read_only_fields = ['id', 'pedido', 'produto']

    def create(self, validated_data):
        validated_data['produto_id'] = validated_data.pop('produto_id')
        return super().create(validated_data)