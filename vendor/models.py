from django.db import models
from accounts.models import User, UserProfile

# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profle = models.OneToOneField(UserProfile, related_name='user_profle', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) # auto_now_add is only sets the field when the object is created 
    modefied_at = models.DateTimeField(auto_now=True) # auto now sets the field when the object is updated or created 



    def __str__(self):
        return self.vendor_name