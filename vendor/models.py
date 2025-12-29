from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_approval_notification

# Create your models here.
class Vendor(models.Model):
  user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
  user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
  vendor_name = models.CharField(max_length=50)
  vendor_slug = models.SlugField(max_length=100, unique=True)
  vendor_license = models.ImageField(upload_to='vendors/license')
  is_approved = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)  
  modified_at = models.DateTimeField(auto_now=True) 

  def __str__(self):
      return self.vendor_name
  
  def save(self, *args, **kwargs):
      if self.pk is not None:
         # Update
         original = Vendor.objects.get(pk=self.pk)
         if original.is_approved != self.is_approved:
            mail_template = 'accounts/emails/admin_approval_email.html'
            context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
            } 
             # Here you can add any action you want to perform when is_approved changes
            if self.is_approved == True:
                # Send approval notification
                mail_subject = 'Congratulations! Your restaurant has been approved'
                send_approval_notification(mail_subject, mail_template, context)                 
            else:
              # Send disapproval notification
              mail_subject = 'Notification: Your restaurant approval has been revoked'
              send_approval_notification(mail_subject, mail_template, context)
      
      return super(Vendor, self).save(*args, **kwargs)
  
