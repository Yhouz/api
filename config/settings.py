"""
Django settings for config project.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-fd_cs#2m%^sqv8dk%^2*bgkw%#zvylmy=ymph!zt@wjyp=psuk'

# ## MODIFICADO ##: Para produção no Render, é recomendado que DEBUG seja False.
# Ele será True localmente se a variável de ambiente DEBUG_VALUE não estiver definida ou for 'true'.
DEBUG = os.environ.get('DEBUG_VALUE', 'True').lower() == 'true'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
if os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
    ALLOWED_HOSTS.append(os.environ.get('RENDER_EXTERNAL_HOSTNAME'))
# ## MODIFICADO ##: Para garantir que o Render.com funcione corretamente em produção,
# adicione o hostname do Render aos ALLOWED_HOSTS para o modo DEBUG=False também.
if not DEBUG and os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
    ALLOWED_HOSTS.append(os.environ.get('RENDER_EXTERNAL_HOSTNAME'))


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    'corsheaders',
    'api', # Seu custom app
    'storages', # Mantenha 'storages' aqui
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'neondb',
        'USER': 'neondb_owner',
        'PASSWORD': 'npg_BmY8VfO7KPDN',
        'HOST': 'ep-plain-tooth-a8stnpvb-pooler.eastus2.azure.neon.tech',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- STATIC AND MEDIA FILES CONFIGURATION (MODIFIED) ---

# Configurações para AWS S3
# Certifique-se de definir estas variáveis de ambiente no Render!
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
# ## MODIFICADO ##: Use os.environ.get para a região também
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')

# ## MODIFICADO ##: Calcule AWS_S3_CUSTOM_DOMAIN apenas se o nome do bucket estiver disponível
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com' if AWS_STORAGE_BUCKET_NAME else None

# Definições de URL e ROOT para STATIC
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Definições de URL e ROOT para MEDIA (Arquivos enviados por usuários)
# ## MODIFICADO ##: Lógica condicional para MEDIA_URL e MEDIA_ROOT
if DEBUG:
    # Em ambiente de desenvolvimento, use o sistema de arquivos local
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    # Em produção, use o S3. MEDIA_ROOT não é usado com S3.
    if AWS_S3_CUSTOM_DOMAIN:
        # ## MODIFICADO ##: Se seus arquivos no S3 estão em 'media/produtos/',
        # e o campo `imagem` do seu modelo retorna `produtos/nome_da_imagem.jpg`,
        # então o `MEDIA_URL` base deve ser a raiz do seu bucket.
        # Caso contrário, se `imagem` retorna `/produtos/nome_da_imagem.jpg` (com barra inicial),
        # e você quer o `media/` no S3, mantenha o `/media/` aqui.
        # Para o caso `https://None.s3.amazonaws.com/media/produtos/...`, o seu Django
        # está adicionando `/media/` no caminho do S3. Então, mantenha `/media/` aqui.
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    else:
        # Fallback se as variáveis de ambiente S3 não estiverem definidas em produção
        # Isso pode acontecer se você esquecer de definir as variáveis no Render.
        # As imagens não carregarão, mas o Django não quebrará.
        MEDIA_URL = '/media/'
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ## MODIFICADO ##: Configuração consolidada de STORAGES para Django 4.0+
STORAGES = {
    "default": { # Para arquivos de mídia (uploads de usuário)
        # ## MODIFICADO ##: Usa S3Boto3Storage para uploads de usuário em produção.
        # Em DEBUG, o Django usará o FileSystemStorage definido por MEDIA_ROOT.
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage" if not DEBUG else "django.core.files.storage.FileSystemStorage",
        # Adicione estas configurações para o S3Boto3Storage
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "region_name": AWS_S3_REGION_NAME,
            "access_key_id": AWS_ACCESS_KEY_ID,
            "secret_access_key": AWS_SECRET_ACCESS_KEY,
            "custom_domain": AWS_S3_CUSTOM_DOMAIN,
            "location": "media", # Isso vai criar uma pasta 'media/' dentro do seu bucket S3
            # Se você já tem CORS configurado no bucket S3, pode ser necessário especificar headers
            # "file_overwrite": False, # Evita sobrescrever arquivos com o mesmo nome (geralmente bom)
        },
    },
    "staticfiles": { # Para arquivos estáticos (CSS, JS, etc.)
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ## REMOVER ##: Esta linha é redundante e pode causar conflito com o dicionário STORAGES.
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# --- END STATIC AND MEDIA FILES CONFIGURATION ---

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True # ## AVISO DE SEGURANÇA ##: Em produção, considere restringir para domínios específicos.

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

}

SIMPLE_JWT = {
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'ALGORITHM': 'HS256',
}
AUTH_USER_MODEL = 'api.Usuario' # Certifique-se que 'api' é o nome do seu app

# ## REMOVER ##: Esta parte está duplicada da seção de STATIC AND MEDIA FILES CONFIGURATION.
# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = 'us-east-1' # Sua região do S3
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com' # Ou seu CDN se usar um
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'