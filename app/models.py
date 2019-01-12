from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.
class Neighborhood(models.Model):
    name = models.CharField(max_length=40, null=True, blank=True)
    location=models.CharField(max_length=100, null=True, blank=True)
    description = HTMLField()
    photo = models.ImageField(upload_to='profpics/',default='profpics/default.jpg')
    user = models.ForeignKey(User, null=True)

    def create_neighborhood(self):
        self.save()

    def delete_neighborhood(self):
        self.delete()

    @classmethod
    def find_neighborhood(cls,search_term):
        hood = cls.objects.filter(name__icontains = search_term)

    @classmethod
    def update_neighborhood(cls,id ,name, description ,location,photo):
        updated_neighborhood = cls.objects.filter(id = id).update(name = name, description = description ,location = location,category = category,photo=photo)
    def __str__(self):
        return self.name


class Profile(models.Model):
    bio = HTMLField(default="majiriani wema")
    photo = models.ImageField(upload_to='profpics/',default='profpics/prof.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wewe",primary_key=True)
    neighborhood=models.ForeignKey(Neighborhood, on_delete=models.CASCADE,null=True,blank=True,related_name="members")
    email = models.CharField(max_length=60,blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.wewe.save()

    def __str__(self):
        return self.user.username

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def filter_by_id(cls, id):
        profile = Profile.objects.filter(user = id).first()
        return profile
    @classmethod
    def get_by_id(cls, id):
        profile = Profile.objects.get(user = id)
        return profile
class Business(models.Model):
    name=models.CharField(max_length=40, null=True, blank=True)
    propreiter=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    neighborhood=models.ForeignKey(Neighborhood, on_delete=models.CASCADE,null=True,blank=True,related_name="businesses")
    email = models.EmailField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    def create_business(self):
        self.save()

    def delete_business(self):
        self.delete()

    @classmethod
    def search_by_name(cls,search_term):
    	businesses = cls.objects.filter(name__icontains=search_term)
    	return businesses

    @classmethod
    def update_business(cls,id,name,propreiter,neighborhood,email):
        updated_business=cls.object.filter(id=id).update(name=name,propreiter=propreiter,neighborhood=neighborhood,email=email)


class Alert(models.Model):
    alert=HTMLField()
    posted_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    neighborhood=models.ForeignKey(Neighborhood, on_delete=models.CASCADE,null=True,blank=True,related_name="alerts")
    date_posted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.alert

    def save_alert(self):
        self.save()

    def delete_alert(self):
        self.delete()

    class Meta:
        ordering = ['alert']


class Comment(models.Model):
    comment = HTMLField(default="")
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now=True)
    alert=models.ForeignKey(Alert, on_delete=models.CASCADE,null=True,blank=True,related_name="comments")

    def __str__(self):
        return self.comment

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()
        
    class Meta:
        ordering =['-date_posted']
