import base64
from django.contrib.auth import get_user_model
from io import BytesIO
import sys
from django.core.files import File
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from base64 import  b64decode, b64encode
from cryptography.hazmat.backends import default_backend
from uuid import uuid4
from django.contrib.auth import get_user_model
import base64
from io import BytesIO
from django.core.files import File
import sys

class DataEncryption():

    def encrypt(key, plaintext):
        key                 = key.encode('utf-8')
        iv                  = os.urandom(16)
        cipher              = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor           = cipher.encryptor()
        padder              = PKCS7(128).padder()
        padded_plaintext    = padder.update(plaintext.encode("utf-8")) + padder.finalize()
        ciphertext          = encryptor.update(padded_plaintext) + encryptor.finalize()
        return b64encode(iv + ciphertext).decode("utf-8")

    def decrypt(key, ciphertext):
        key               = key.encode('utf-8')
        ciphertext        = b64decode(ciphertext.encode("utf-8"))
        iv                = ciphertext[:16]
        ciphertext        = ciphertext[16:]
        cipher            = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor         = cipher.decryptor()
        decrypted_padded  = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder          = PKCS7(128).unpadder()
        decrypted_plaintext_padded = unpadder.update(decrypted_padded) + unpadder.finalize()
        plaintext = decrypted_plaintext_padded.decode("utf-8")
        return plaintext
    
def get_object_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None

def get_token_user_or_none(request):
    User = get_user_model()
    try:
        instance = User.objects.get(id=request.user.id)
    except Exception:
        instance = None
    finally:
        return instance
    
class ConvertBase64File():
    
    def base64_to_file(self,value):
        try:
            
            format, base64_data = value.split(';base64,')
            decoded_data = base64.b64decode(base64_data)
            stream = BytesIO()
            stream.write(decoded_data)
            stream.seek(0)
            return File(stream)
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return None
        
        
    def base64_file_extension(self,value):
        try:
            format, base64_data = value.split(';base64,')
            media_type = format.split('/')[1]
            base64_extension = media_type.split('+')[0] 
            return base64_extension

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return None
# class ConvertBase64File():
    
#     def base64toImage(image_data:str):
        
#         if image_data:
#             image_format, imgstr = image_data.split(';base64,')
#         ext = image_format.split('/')[-1]
#         return ContentFile(base64.b64decode(imgstr), name=f'image.{ext}')
    
#     def base64toFile(file_field:str):
        
#         if file_field:
#             pdf_format, pdfstr = file_field.split(';base64,')
#         pdf_ext = pdf_format.split('/')[-1]
#         pdf_content = base64.b64decode(pdfstr)

#         pdf_file = ContentFile(pdf_content, name=f'document.{pdf_ext}')
#         return pdf_file
    
#     def save_base64_file_to_db(base64_data, file_name):
        
#         if base64_data.startswith("data:application/pdf;base64,"):
#             _, base64_data = base64_data.split(',', 1)

#         decoded_data = base64.b64decode(base64_data)
#         content_file = ContentFile(decoded_data, name=file_name)
      
#         return content_file
            
#     def base64toFiledata(file_field: str):
#         if file_field:
#             file_format, file_data = file_field.split(';base64,')
#             file_ext = file_format.split('/')[-1]

#             # Decode the base64 data
#             file_content = base64.b64decode(file_data)

#             # Determine the file name based on the original format
#             file_name = f'document.{file_ext}'

#             # Create a ContentFile with the decoded content and original file name
#             file = ContentFile(file_content, name=file_name)
#             return file
#         return None        

#     def base64toVideo(file_field: str):
#         if file_field:
#             video_format, video_str = file_field.split(';base64,')
#             video_ext = video_format.split('/')[-1]
#             video_content = base64.b64decode(video_str)

#             video_file = ContentFile(video_content, name=f'video.{video_ext}')
#             return video_file