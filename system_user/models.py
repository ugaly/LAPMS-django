from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings




class SystemUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_citizen = models.BooleanField(default=False)
    is_landvaluer = models.BooleanField(default=False)
    is_landofficer = models.BooleanField(default=False)
    is_indemnity_payer = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True)
    thumbnail = models.ImageField(
		upload_to='upload_thumbnail/',
		null=True,
		blank=True
	)

    class Meta:
        verbose_name = 'System User'
        verbose_name_plural = 'System Users'


    def save(self, *args, **kwargs):
        is_new_landvaluer = False
        if self.pk is None and self.is_landvaluer:
            is_new_landvaluer = True
        super().save(*args, **kwargs)
        
        if is_new_landvaluer:
            # Add the user to all existing chat groups
            chat_groups = ChatGroup.objects.all()
            for group in chat_groups:
                group.members.add(self)
                group.save()
    
    def __str__(self):
        return self.full_name


class ChatGroup(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(SystemUser, related_name='chat_groups', blank=True)
    thumbnailUrl = models.ImageField(upload_to='upload_thumbnail/', null=True, blank=True)
    

    def __str__(self):
        return self.name


@receiver(post_save, sender=ChatGroup)
def add_landvaluers_to_group(sender, instance, created, **kwargs):
    if created and not instance.members.exists():
        landvaluers = SystemUser.objects.filter(is_landvaluer=True)
        instance.members.set(landvaluers)



class Message(models.Model):
    chat_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} in {self.chat_group.name} at {self.timestamp}'
    



class Shapefile(models.Model):
    name = models.CharField(max_length=255)
    shp_file = models.FileField(upload_to='shapefiles/')
    uploaded_at = models.DateTimeField(auto_now_add=True)