from django.shortcuts import render,redirect
from django.http  import HttpResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Image, Profile, Comments
from django.contrib.auth.models import User
from .forms import ImageForm, ProfileForm, CommentForm
 
# Create your views here.
 
 
 
@login_required(login_url='/accounts/login/')
def home(request): 
    title = 'Home' 
    images = Image.get_all_images()
    return render(request, 'home.html', {'title':title,'images':images})



def profile (request):
    current_user=request.user
    
    # images=Image.get_profile_images(profile_id)
    profile_details= Profile.objects.filter(id=current_user.profile.id)
    print(current_user.profile.id)
    

    return render(request,'profile.html',{'profile':profile,'profile_details':profile_details,'images':images})

 





@login_required(login_url='/accounts/login')
def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.profile = request.user            
            upload.save()
            return redirect('profile',username=request.user)
    #         return redirect('profile')
    else:
        form = ImageForm()
    
    return render(request, 'upload.html', {'form':form})


@login_required(login_url='/accounts/login')
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.user = request.user
            edit.save()
            return redirect('profile')
            print(edit)
    else:
        form = ProfileForm()

    return render(request,'edit_profile.html', {'form':form})





 