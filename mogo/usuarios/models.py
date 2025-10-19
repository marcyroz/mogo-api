from django.db import models
import uuid
# Usuario, PCD e Terceiro models


class Usuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    foto_perfil = models.ImageField(
        upload_to='fotos_perfil/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # ========== ATRIBUTOS OBRIGATÓRIOS PARA AUTH_USER_MODEL ==========
    USERNAME_FIELD = 'email'  # Campo usado para login
    # Campos obrigatórios além do USERNAME_FIELD e password
    REQUIRED_FIELDS = ['nome']

    # Para compatibilidade com Django Admin
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    # ==================================================================

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['nome']),
        ]
        constraints = [                          # Segurança
            models.CheckConstraint(
                check=models.Q(deleted_at__isnull=True) |
                models.Q(deleted_at__gte=models.F('created_at')),
                name='valid_deletion_date'
            )
        ]

    def __str__(self):
        return self.nome

# ========== PROPRIEDADES NECESSÁRIAS PARA JWT ==========

    @property
    def is_authenticated(self):
        """Sempre retorna True para usuários válidos"""
        return True

    @property
    def is_anonymous(self):
        """Sempre retorna False para usuários autenticados"""
        return False

    @property
    def is_active(self):
        """Verifica se a conta não foi desativada (soft delete)"""
        return self.deleted_at is None

    # Necessário para o JWT identificar o usuário
    def get_username(self):
        """Retorna o identificador único do usuário (email neste caso)"""
        return self.email

    # ========== MÉTODOS PARA COMPATIBILIDADE COM ADMIN ==========

    def has_perm(self, perm, obj=None):
        """Verifica se o usuário tem uma permissão específica"""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Verifica se o usuário tem permissões para acessar um app"""
        return self.is_superuser

    # ======================================================


class PCD(models.Model):

    TIPOS_DEFICIENCIA = [
        ('fisica', 'Física'),
        ('visual', 'Visual'),
        ('auditiva', 'Auditiva'),
        ('intelectual', 'Intelectual'),
        ('multipla', 'Múltipla'),
    ]

    FORMA_LOCOMOCAO = [
        ('andar', 'Andar'),
        ('cadeira_rodas', 'Cadeira de Rodas'),
        ('muletas', 'Muletas'),
        ('andador', 'Andador'),
        ('outro', 'Outro'),
    ]

    RECURSOS_ACESSIBILIDADE = [
        ('rampas', 'Rampas'),
        ('pisos_tateis', 'Pisos Táteis'),
        ('elevadores', 'Elevadores'),
        ('outros', 'Outros Recursos'),
    ]

    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name='pcd')
    tipo_deficiencia = models.CharField(
        max_length=20,
        choices=TIPOS_DEFICIENCIA
    )
    forma_locomocao = models.CharField(
        max_length=50, choices=FORMA_LOCOMOCAO, default='andar')
    recursos_acessibilidade = models.JSONField(default=list)
    detalhes = models.TextField(
        null=True, blank=True, default='', max_length=500)

    class Meta:
        db_table = 'pcds'
        verbose_name = 'Pessoa com Deficiência'
        verbose_name_plural = 'Pessoas com Deficiência'
        ordering = ['tipo_deficiencia']

    def __str__(self):
        return f"PCD - {self.usuario.nome}"


class Terceiro(models.Model):

    TIPOS_RELACAO = [
        ('familiar', 'Familiar'),
        ('cuidador', 'Cuidador Profissional'),
        ('amigo', 'Amigo'),
        ('voluntario', 'Voluntário'),
        ('outro', 'Outro'),
    ]

    TIPO_DEFICIENCIA_ASSISTIDA = [
        ('fisica', 'Física'),
        ('visual', 'Visual'),
        ('auditiva', 'Auditiva'),
        ('intelectual', 'Intelectual'),
        ('multipla', 'Múltipla'),
    ]

    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name='terceiro')
    relacao = models.CharField(max_length=20, choices=TIPOS_RELACAO)
    pcd_assistida_tipo_deficiencia = models.CharField(
        max_length=20, choices=TIPO_DEFICIENCIA_ASSISTIDA)
    descricao = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'terceiros'
        verbose_name = 'Terceiro Responsável'
        verbose_name_plural = 'Terceiros Responsáveis'
        ordering = ['relacao']

    def __str__(self):
        return f"Terceiro - {self.usuario.nome}"
