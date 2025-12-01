from django.db.models.signals import post_save, pre_save
from accounts.models import UserProfile, User


def post_save_create_profile_receiver(sender, instance, created,**kwargs):
  if created:
    UserProfile.objects.create(user=instance)
  else:
    try: 
      profile = UserProfile.objects.get(user=instance)
      profile.save()      
    except:
      # create the userprofile if not exists
      UserProfile.objects.create(user=instance)
      print('Profile created!')
    print("User updated!")

def pre_save_create_profile_receiver(sender, instance, **kwargs):
  print(instance.username, "this user is being saved!") 


#post_save gets triggered after save
post_save.connect(post_save_create_profile_receiver, sender=User)
# pre_save gets triggered before saving
pre_save.connect(pre_save_create_profile_receiver, sender=User)