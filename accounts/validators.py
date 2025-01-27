from django.core.exceptions import ValidationError
import os 


def allowOnlyImagesValidator(value):
    ext = os.path.splitext(value.name)[1]
    print(ext)
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if not ext.lower() in valid_extensions:
            raise ValidationError(message='Unsupported File extension, Allowed Extension' + str(valid_extensions))
