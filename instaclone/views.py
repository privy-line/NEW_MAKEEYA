from django.shortcuts import render,redirect
from django.http  import HttpResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Image, Profile, Comments
from django.contrib.auth.models import User
from .forms import ImageForm, ProfileForm, CommentsForm
 
# Create your views here.
 
 
 
@login_required(login_url='/accounts/login/')
def home(request): 
    title = 'Home' 
    images = Image.get_all_images()
    return render(request, 'home.html', {'title':title,'images':images})



def profile (request):
    current_user=request.user
    
    # images=Image.get_profile_images(profile_id)
    profile_details=  Profile.objects.get(user=current_user.id)    
    print(profile_details.prof_pic)
    images=Image.get_profile_images(profile_details.user_id)

    return render(request,'profile.html',{'profile':profile,'profile_details':profile_details,'images':images})

 


@login_required(login_url='/accounts/login')
def upload_image(request):
    current_user=request.user
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.profile = current_user           
            upload.save()
            return redirect('profile')
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


def comments(request,id):
        current_user = request.user
        
        post = Image.objects.get(id=id)
        comments = Comments.objects.filter(image=post)
        # print(comments)
        if request.method == 'POST':
                form = CommentsForm(request.POST,request.FILES)
                if form.is_valid():
                        comment = form.cleaned_data['comment']
                        new_comment = Comments(comment = comment,user =current_user,image=post)
                        new_comment.save() 

                        return redirect('home')                   
                
        else:
                form = CommentsForm()
        return render(request, 'comment.html', {"form":form,'post':post,'user':current_user,'comments':comments})




def view_comments(request):
    current_user=request.user   
    post = Image.objects.get(id=id)    
    image_comments= Comments.objects.filter(image=post)    
    return render(request,'home.html',{'image_comments':image_comments, 'post':post,'user':current_user})

 