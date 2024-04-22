from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

def validate_video(value):
  
    file_size = value.size
    if file_size > 5242880:
        raise ValidationError("The maximum file size that can be uploaded is 5MB")
    file_type = value.content_type.split('/')[0]
    if file_type != 'video':
        raise ValidationError("Only video files can be uploaded")