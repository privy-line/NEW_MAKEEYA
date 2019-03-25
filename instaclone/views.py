from django.shortcuts import render
from django.http  import HttpResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Image, Profile, Comments
# Create your views here.
 
 
 
@login_required(login_url='/accounts/login/')
def home(request): 
    title = 'Home' 
    images = Image.get_all_images()
    return render(request, 'home.html', {'title':title,'images':images})

@login_required(login_url='/accounts/login/')
def profile(request): 
    return render(request,'profile.html')

@login_required(login_url='/accounts/login')
def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.profile = request.user
            # print(f'image is {upload.image}')
            upload.save()
            return redirect('profile', username=request.user)
    else:
        form = ImageForm()
    
    return render(request, 'profile/upload_image.html', {'form':form})




 