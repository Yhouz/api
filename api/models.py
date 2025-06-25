
from tkinter.tix import STATUS
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager # ✅ Importar essas classes

# --- CUSTOM USER MANAGER ---
# Esta classe é necessária para dizer ao Django como criar um usuário e um superusuário
class CustomUserManager(BaseUserManager):
    def create_user(self, email, nome, cpf, tipo_usuario, senha=None, **extra_fields):
        if not email:
            raise ValueError('O campo de Email deve ser definido')
        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, cpf=cpf, tipo_usuario=tipo_usuario, **extra_fields)
        user.set_password(senha) # Usa o método set_password para hashear a senha
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, cpf, tipo_usuario='admin', senha=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True) # Superusuário sempre ativo

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, nome, cpf, tipo_usuario, senha, **extra_fields)


TIPOS = (
    ('cliente', 'Cliente'),
    ('funcionario', 'Funcionario'),
    ('admin', 'Administrador'),
)

# --- USUARIO MODEL ---
# ✅ Herdar de AbstractBaseUser e PermissionsMixin
class Usuario(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128) # Campo para armazenar a senha hasheada (não vamos mais usar make_password diretamente aqui)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS)
    saldo_carteira = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True) # ✅ Já existia, mas é importante para AbstractBaseUser
    is_staff = models.BooleanField(default=False) # ✅ Adicione este campo para PermissionsMixin

    # ✅ Esses campos são MANDATÓRIOS para AbstractBaseUser
    USERNAME_FIELD = 'email'  # O campo que será usado para login
    REQUIRED_FIELDS = ['nome', 'cpf', 'tipo_usuario'] # Campos obrigatórios para criar superusuários via `createsuperuser`

    # ✅ Conecta seu CustomUserManager ao seu modelo Usuario
    objects = CustomUserManager()

    def __str__(self):
        return self.nome

    # ✅ Adicione este método, essencial para AbstractBaseUser.
    # O Django o usa internamente para verificar permissões de staff/admin.
    # Embora PermissionsMixin lide com `is_superuser`, `is_staff` é importante aqui.
    # Você já tem `is_staff = models.BooleanField(default=False)` acima.
    def has_perm(self, perm, obj=None):
        return self.is_superuser # Ou implemente uma lógica mais granular de permissão

    def has_module_perms(self, app_label):
        return self.is_superuser # Ou implemente uma lógica mais granular de permissão

    # Nota: is_anonymous e is_authenticated são propriedades padrão fornecidas por AbstractBaseUser.
    # Você não precisa implementá-las diretamente.


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

#Carrinho de Compras

class Carrinho(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='carrinhos')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    finalizado = models.BooleanField(default=False)  # Para saber se já virou um pedido

    def __str__(self):
        return f"Carrinho de {self.usuario.nome} - {self.criado_em.strftime('%d/%m/%Y %H:%M')}"

    def total_itens(self):
        return sum(item.quantidade for item in self.itens.all())

    def total_valor(self):
        return sum(item.subtotal() for item in self.itens.all())


class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"

    def subtotal(self):
        return self.quantidade * self.produto.preco

## Pedido 

STATUS = (  # noqa: F811
    ('pendente', 'Pendente'),
    ('entregue', 'Entregue'),
)

class Pedido(models.Model):
    pedido_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pedidos')
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name='pedido', unique=True)
    data_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status_pedido = models.CharField(max_length=20, choices= STATUS)  # Ex: Pendente, Em Preparação, Entregue
    qr_code_pedido = models.CharField(max_length=100, blank=True, null=True)  # Para armazenar o QR Code do pedido

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario.nome} - {self.data_pedido.strftime('%d/%m/%Y %H:%M')}"

class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} - Pedido {self.pedido.id}"
    
    def subtotal(self):
        return self.quantidade * self.produto.preco

