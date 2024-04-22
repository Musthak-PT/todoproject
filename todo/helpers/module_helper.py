import os
from pathlib import Path
from django.shortcuts import get_object_or_404
from django.core.files.temp import NamedTemporaryFile
from urllib.parse import urlparse
import urllib.request
from django.core.files import File
from django.core.files.storage import default_storage


def imageDeletion(request,image_del):
    try:
        base_path = Path(__file__).resolve().parent.parent.parent.parent
        if image_del.image:
            if os.path.exists(str(base_path) + str(image_del.image.url)):
                image_del.image.delete()
        image_del.delete()
    except Exception as e:
        pass


