from django.db.models.signals import post_save, post_delete 
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.models import User




def deleteuser(sender,instance ,**kwargs):
    user=instance.user
    user.delete()
    print('Deleting User') 


def updateUser(sender,instance,created,**kwargs):
    profile =instance
    user = profile.user
    if created == False :
        user.first_name=profile.name
        user.username=profile.username
        user.email=profile.email
        user.save()



#@receiver(post_save,sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user =user,
            username = user.username,
            email = user.email,
            name= user.first_name,
        )


post_save.connect(createProfile, sender=User)
post_delete.connect(deleteuser, sender=Profile)
post_save.connect(updateUser,sender=Profile)