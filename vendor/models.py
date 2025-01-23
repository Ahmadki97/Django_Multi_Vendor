from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import sendNotificationMail

# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='user_profle', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) # auto_now_add is only sets the field when the object is created 
    modefied_at = models.DateTimeField(auto_now=True) # auto now sets the field when the object is updated or created 



    def __str__(self):
        return self.vendor_name
    

    def save(self, *args, **kwargs):
        if self.pk is not None:
            print(self.pk)
            orig = Vendor.objects.get(pk=self.pk)
            print(f"Original is_approved: {orig.is_approved}, Current is_approved: {self.is_approved}")
            if orig.is_approved != self.is_approved:
                print(f"Second if executed")
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved
                }
                if self.is_approved == True:
                    mail_subject = "Congratulations, Your resturan has been approved."
                    sendNotificationMail(mail_subject=mail_subject, mail_template=mail_template, context=context)
                else:
                    mail_subject = 'We Are sorry! you are not eligible for publishing your food menu on our marketplace'
                    sendNotificationMail(mail_subject=mail_subject, mail_template=mail_template, context=context)
        return super(Vendor, self).save(*args, **kwargs) 