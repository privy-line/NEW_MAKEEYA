from django.db import models
from django.contrib.auth.models import User  
from tinymce.models import HTMLField
 


# Create your models here.
class Image(models.Model):
    name = models.CharField(max_length = 50)
    caption = models.CharField(max_length=100)     
    profile = models.ForeignKey(User,on_delete=models.CASCADE)   
    upload_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='profile')
    likes = models.BooleanField(default=False)
   

    class Meta:
        ordering = ('upload_date',)

    def save_image(self):
        self.save()
    
    @classmethod
    def update_caption(cls, update):
        pass
    
    @classmethod
    def get_image_id(cls, id):
        image = Image.objects.get(pk=id)
        return image
    
    @classmethod
    def get_profile_images(cls, profile):
        images = Image.objects.filter(profile__pk = profile)
        return images
    
    @classmethod
    def get_all_images(cls):
        images = Image.objects.all()
        return images


class Profile(models.Model):
    prof_pic = models.ImageField(upload_to='profile/',blank=True)
    bio = HTMLField()
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)


    def save_profile(self):
        self.save()
    
    @classmethod
    def search_profile(cls, name):
        profile = Profile.objects.filter(user__username__icontains = name)
        return profile
    
    @classmethod
    def get_by_id(cls, id):
        profile = Profile.objects.get(user = id)
        return profile

    @classmethod
    def filter_by_id(cls, id):
        profile = Profile.objects.filter(user = id).first()
        return profile

 


class Comments(models.Model):
    comment = HTMLField()
    posted_on = models.DateTimeField(auto_now=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save_comment(self):
        self.save()
    
    @classmethod
    def get_comments_by_images(cls, id):
        comments = Comments.objects.filter(image__pk = id)
        return comments