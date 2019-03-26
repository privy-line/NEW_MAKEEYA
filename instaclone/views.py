from django.shortcuts import render
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

def profile(request, username):
    profile = User.objects.get(username=username)
    # print(profile.id)
    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)
    images = Image.get_profile_images(profile.id)
    title = f'@{profile.username} Instagram photos and videos'

    return render(request, 'profile/profile.html', {'title':title, 'profile':profile, 'profile_details':profile_details, 'images':images})




# def profile(request,profile_id):  
#     try: 
#             # locations = Location.objects.all()
#             profile = Profile.objects.get(id = profile_id)
#             images = Image.objects.filter(profile = profile.id)    
#     except:        
#             raise Http404()   
#     return render(request,'profile.html',{'profile':profile,'images':images,})





@login_required(login_url='/accounts/login')
def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.profile = request.user            
            upload.save()
            return redirect('profile', username=request.user)
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
            return redirect('edit_profile')
    else:
        form = ProfileForm()

    return render(request,'edit_profile.html', {'form':form})





 