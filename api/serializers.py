from rest_framework import serializers
from .models import Cardapio, Usuario, Funcionario, Produto, Fornecedor


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