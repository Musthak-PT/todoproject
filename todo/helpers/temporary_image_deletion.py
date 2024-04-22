import os
from pathlib import Path
from django.shortcuts import get_object_or_404
from django.core.files.temp import NamedTemporaryFile
from urllib.parse import urlparse
import urllib.request
from django.core.files import File
from django.core.files.storage import default_storage

def ImageDeletion(request, product_image_del, action_type):
    try:
        base_path = Path(__file__).resolve().parent.parent.parent.parent
        if action_type == '1':
            if product_image_del.property_image:
                if os.path.exists(str(base_path) + str(product_image_del.property_image.url)):
                    product_image_del.property_image.delete()
        elif action_type == '2':
            if product_image_del.image:
                if os.path.exists(str(base_path) + str(product_image_del.image.url)):
                    product_image_del.image.delete()
        product_image_del.delete()
    except Exception as e:
        pass

