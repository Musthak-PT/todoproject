from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.authentication.models import AbstractDateFieldMix
from apps.users.models import Users
from random import randint
from django.utils.text import slugify

def default_image():
    return f"default/image/default-image.png"  


def our_projects_image_media(self, filename):
    extension = filename.split('.')[-1].lower()
    upload_path = 'assets/our-projects/'
    return '{}{}.{}'.format(upload_path, uuid4(), extension)

def our_clients_image_media(self, filename):
    extension = filename.split('.')[-1].lower()
    upload_path = 'assets/our-clients/'
    return '{}{}.{}'.format(upload_path, uuid4(), extension)

def our_servicer_image_media(self, filename):
    extension = filename.split('.')[-1].lower()
    upload_path = 'assets/our-service/'
    return '{}{}.{}'.format(upload_path, uuid4(), extension)

def default_blog_og_image():
    return f"default/blog/default_bog_og_image.png"

def seo_blog_image_media(self, filename):
    return 'assets/seo-blog-image/{}.png'.format(self.meta_image_title, uuid4())


def blog_image_media(self, filename):
    extension = filename.split('.')[-1].lower()
    upload_path = 'assets/blog-image/'
    return '{}{}.{}'.format(upload_path, uuid4(), extension)

def tech_stack_image_media(self, filename):
    return f"assets/tech-stack/{self.id}/{self.stack_title}.png"

