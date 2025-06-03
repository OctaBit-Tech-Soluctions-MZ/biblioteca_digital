from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class BlockedUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="block_user")
    reason = models.TextField()
    is_blocked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 


class Document(models.Model):
    TYPE_CHOICES = [
        ('livros', 'Livros'),
        ('artigos','Artigos'),
        ('teses', 'Teses'),
        ('revistas', 'Revistas')
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    year = models.IntegerField()
    link = models.FileField(upload_to='documentos/')
    description = models.TextField()
    isdownloaded = models.BooleanField(default=False)
    slug = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='livros')
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title

class Order(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pendente")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido #{self.id} (Usuário {self.user.username})"

class Statistic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='statistics')
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='statistics')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Estatística #{self.id} (Usuário {self.user.username})"
