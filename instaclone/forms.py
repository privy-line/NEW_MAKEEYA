from django import forms 
from django.contrib.auth.models import User
from .models import Image, Profile, Comments


class ImageForm(forms.ModelForm):  
    class Meta:
        model = Image
        exclude = ['likes', 'post_date', 'profile']
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class CommentsForm(forms.Form):     
       comment=forms.CharField(label='Comment',max_length=100)
       