from rest_framework import serializers
from .models import Cardapio, Carrinho, ItemCarrinho, Usuario, Funcionario, Produto, Fornecedor


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

# ✅ ItemCarrinhoSerializer: ESTA É A CHAVE PARA O TYPERROR!
class ItemCarrinhoSerializer(serializers.ModelSerializer):
    # ESTE CAMPO É PARA LEITURA (quando o backend ENVIA dados para o frontend, GET requests)
    # Ele DEVE serializar o OBJETO Produto COMPLETO usando ProdutoSerializer.
    produto = ProdutoSerializer(read_only=True)

    # ESTE CAMPO É PARA ESCRITA (quando o frontend ENVIA dados para o backend, POST/PUT requests)
    # Ele aceita um ID e mapeia para o campo 'produto' do modelo ItemCarrinho.
    produto_id = serializers.PrimaryKeyRelatedField(
        queryset=Produto.objects.all(), # Define os produtos válidos
        source='produto',              # Mapeia para o campo 'produto' do modelo
        write_only=True                # Indica que este campo é apenas para entrada
    )

    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = ItemCarrinho
        # AMBOS 'produto' e 'produto_id' devem estar em 'fields'.
        # O DRF é inteligente para usar 'produto' na saída e 'produto_id' na entrada.
        fields = ['id', 'carrinho', 'produto', 'produto_id', 'quantidade', 'subtotal']
        read_only_fields = ['id', 'subtotal']

    def get_subtotal(self, obj):
        return obj.subtotal()

    def validate(self, data):
        carrinho_instance = data.get('carrinho')
        # Quando 'produto_id' é fornecido na entrada, o DRF resolve-o para a instância 'produto'
        # e a coloca no 'data'. Então, 'data.get('produto')' aqui já deve ser a instância.
        produto_instance = data.get('produto')
        quantidade = data.get('quantidade', 0)

        request = self.context.get('request')
        if not request or not hasattr(request, 'user') or not request.user.is_authenticated:
            raise serializers.ValidationError({"auth": "Usuário não autenticado para adicionar item ao carrinho."})
        
        if not carrinho_instance:
            raise serializers.ValidationError({"carrinho": "O ID do carrinho é obrigatório e deve ser válido."})
        
        if carrinho_instance.usuario.id != request.user.id:
            raise serializers.ValidationError(
                {"carrinho": "Você não tem permissão para adicionar itens a este carrinho."}
            )
        
        # A validação para 'produto' verifica a instância
        if not produto_instance:
             raise serializers.ValidationError({"produto_id": "Produto não encontrado ou ID inválido."})

        if quantidade <= 0:
            raise serializers.ValidationError({"quantidade": "A quantidade deve ser maior que zero."})
        
        if produto_instance.quantidade_estoque < quantidade:
            raise serializers.ValidationError({"quantidade": f"Estoque insuficiente para {produto_instance.nome}. Disponível: {produto_instance.quantidade_estoque}"})

        return data



    
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