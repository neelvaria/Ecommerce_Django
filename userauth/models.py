from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True,null=False)
    username = models.CharField(max_length=50)
    bio = models.CharField(max_length=100)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username
    
class contactus(models.Model):
    full_name = models.CharField(max_length=100, null=False, blank=False)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField()
    message = models.TextField()
    subject = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        verbose_name = "Contact us"
        verbose_name_plural = "Contact Us"
    
    def __str__(self):
        return self.full_name
    
class profile_details(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_Details')
    full_name = models.CharField(max_length=100, null=False, blank=False)
    bio = models.CharField(max_length=100)
    phone = models.CharField(max_length=25, null=True, blank=True)
    verified = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Profile Details"
        verbose_name_plural = "Profile Details"
    
    def __str__(self):
        return self.full_name
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile_details.objects.create(user=instance)
    
def save_user_profile(sender, instance, **kwargs):
    instance.profile_details.save()
    
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
