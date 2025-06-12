from django.contrib.auth.models import AbstractUser,Group
from django.db import models

# User = get_user_model()


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self) :
        return self.name
    
class User(AbstractUser):
    student_code = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=10)
    course = models.ForeignKey(Course, blank=True, null=True, on_delete=models.SET_NULL)
    
class Subject(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,related_name='subject_to_course')
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name
    
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
    slug = models.SlugField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='livros')
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="documento_to_course")
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
    copy_total = models.IntegerField()
    first_page = models.IntegerField()
    last_page = models.IntegerField()
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pendente")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido #{self.id} (Usuário {self.user.username})"

class BlockedUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="block_user")
    reason = models.TextField()
    is_blocked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.reason

class AcessDocStatistic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='statistics_user')
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='statistics_doc')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Estatística #{self.id} (Usuário {self.user.username})"
    
class DocumentGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, related_name="document_group_permissios")
    document = models.ForeignKey(Document, on_delete=models.DO_NOTHING, related_name="group_document_permissions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)