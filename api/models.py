







from django.db import models


TIPOS = (
    ('cliente', 'Cliente'),
    ('funcionario', 'Funcionario'),
    ('admin', 'Administrador'),
)


class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS)
    saldo_carteira = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

CARGO = (
    ('gerente', 'Gerente'),
    ('caixa', 'Caixa'),
    ('atendente', 'Atendente'),
    ('cozinheiro', 'Cozinheiro'),
    ('estoquista', 'Estoquista'),
    ('administrador', 'Administrador'),
    ('faxineiro', 'Faxineiro'),
)

UF = (
    ('Acre', 'AC'),
    ('Alagoas', 'AL'),
    ('Amapá', 'AP'),
    ('Amazonas', 'AM'),
    ('Bahia', 'BA'),
    ('Ceará', 'CE'),
    ('Distrito Federal', 'DF'),
    ('Espírito Santo', 'ES'),
    ('Goiás', 'GO'),
    ('Maranhão', 'MA'),
    ('Mato Grosso', 'MT'),
    ('Mato Grosso do Sul', 'MS'),
    ('Minas Gerais', 'MG'),
    ('Pará', 'PA'),
    ('Paraíba', 'PB'),
    ('Paraná', 'PR'),
    ('Pernambuco', 'PE'),
    ('Piauí', 'PI'),
    ('Rio de Janeiro', 'RJ'),
    ('Rio Grande do Norte', 'RN'),
    ('Rio Grande do Sul', 'RS'),
    ('Rondônia', 'RO'),
    ('Roraima', 'RR'),
    ('Santa Catarina', 'SC'),
    ('São Paulo', 'SP'),
    ('Sergipe', 'SE'),
    ('Tocantins', 'TO'),
)



class Funcionario(models.Model):
    id_funcionario = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    cargo = models.CharField(max_length=100, choices=CARGO)
    dt_admissao = models.DateField()
    dt_nascimento = models.DateField()
    salario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    endereco = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=4, null=True, blank=True)
    bairro = models.CharField(max_length=20, null=True, blank=True)
    uf = models.CharField(max_length=19, null=True, blank=True, choices=UF)
    cidade = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.usuario.nome if self.usuario else "Sem usuário"} - {self.cargo}'
    
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_estoque = models.IntegerField()
    categoria = models.CharField(max_length=50)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    categoria = models.CharField(max_length=20, null=True, blank=True )
    custo = models.CharField(max_length=10, null=True, blank=True)
    margem = models.CharField(max_length=10, null=True, blank=True)
    unidade = models.CharField(max_length=10, null=True, blank=True)

    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
   
    

    def __str__(self):
        return self.nome
    
    
class Fornecedor(models.Model):
   
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    cidade = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)  # Sigla do estado
    cep = models.CharField(max_length=10, blank=True, null=True)
    contato = models.CharField(max_length=100, blank=True, null=True)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True, null=True)
    class Meta:
        verbose_name = 'Fornecedor'

    def __str__(self):
        return self.nome
    
class Cardapio(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    data = models.DateField()
    imagem = models.ImageField(upload_to='cardapios/', blank=True, null=True)
    # O CAMPO CHAVE: Certifique-se de que é um ManyToManyField
    produtos = models.ManyToManyField(Produto)
    # ... outros campos do Cardapio

    def __str__(self):
        return f"{self.nome} ({self.data})"
    


