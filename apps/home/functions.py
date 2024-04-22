from django.core.files.base import ContentFile
import base64


class ConvertBase64File(): 
    def base64toImage(image_data:str):

        if image_data:
            image_format, imgstr = image_data.split(';base64,')
            ext = image_format.split('/')[-1]
            return ContentFile(base64.b64decode(imgstr), name=f'image.{ext}')
    
    
