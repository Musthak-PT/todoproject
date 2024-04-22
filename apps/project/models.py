from django.db import models
from todo.models import AbstractDateTimeFieldBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from random import randint
from uuid import uuid4
# Create your models here.

class Project(AbstractDateTimeFieldBaseModel):
    slug    = models.SlugField(_('Slug'), max_length=100, editable=False, null=True, blank=True)
    title   = models.CharField(max_length=256)
    class Meta: 
        verbose_name          = "Project"
        verbose_name_plural   = "Project"
        
    def save(self, *args, **kwargs):
        if not self.slug or self.title:
            self.slug = slugify(str(self.title))
            if Project.objects.filter(slug=self.title).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.title)) + '-' + str(randint(1, 9999999))
        super(Project, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
class Todo(AbstractDateTimeFieldBaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    slug          = models.SlugField(_('Slug'), max_length=100, editable=False, null=True, blank=True)
    todo_title    = models.CharField(max_length=256, null=True,blank=True)
    description   = models.TextField(null=True,blank=True)
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    project       = models.ForeignKey(Project, related_name='todos', on_delete=models.CASCADE)
    class Meta: 
        verbose_name          = "Todo Project"
        verbose_name_plural   = "Todo Project"
        
    def save(self, *args, **kwargs):
        if not self.slug or self.id:
            self.slug = slugify(str(self.id))
            if Todo.objects.filter(slug=self.id).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.id)) + '-' + str(randint(1, 9999999))
        super(Todo, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.id