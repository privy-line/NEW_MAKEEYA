from .forms import CartAddProductForm
from django.shortcuts import render,redirect,get_object_or_404
from django.http  import HttpResponse,HttpResponseRedirect,HttpRequest
from django.contrib.auth.decorators import login_required
from .models import Item, Profile,Request,Buyer,Cart
from django.contrib.auth.models import User
from .forms import ImageForm, ProfileForm, BuyerLoginForm,RequestForm,BuyerForm
from .email import send_notification_email
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_POST

# from django.template import Context


 
 
 
 

def home(request): 
    title = 'Home' 
    # category = None
    # categories = Category.objects.all()
    # item = Item.objects.get(id)
    items = Item.get_all_items()
    # if category_slug:
    #     category = get_object_or_404(Category, slug=category_slug)
    #     products = Product.objects.filter(category=category)

    # context = {
    #     'category': category,
    #     'categories': categories,
    #     'item': item
    # }
    return render(request, 'home.html', {'title':title,'items':items})


def detail(request, id):
    item = Item.objects.filter(id=id)
    cart_product_form = CartAddProductForm()
    
    return render(request, 'detail.html',{"item": item,"cart_product_form": cart_product_form})


@login_required(login_url='/accounts/login/')
def profile (request):
    current_user=request.user 
     
    profile_details =  Profile.objects.get(user=current_user.id)    
    print(profile_details.business_logo)
    items=Item.get_profile_items(profile_details.user_id)

    return render(request,'profile.html',{'profile':profile,'profile_details':profile_details,'items':items})


@login_required(login_url='/accounts/login')
def create_item(request):
    current_user=request.user
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.profile = current_user           
            upload.save()
            return redirect('profile')
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

 
def buyer_login(request):
    form = BuyerLoginForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            buyer=Buyer.objects.filter(email = form.cleaned_data['email']).first()
            if buyer.password==form.cleaned_data['password']:
                return redirect('home')
    return render(request,'buyer_login.html',{"form":form})

def buyer_registration(request):
   current_user = request.user
   if request.method == 'POST':
        form = BuyerForm(request.POST, request.FILES)
        if form.is_valid():
            buyer = form.save(commit=False)
            buyer.user = current_user
            buyer.save()
        return redirect('buyer_login')
   else:
        form = BuyerForm()
   return render(request, 'buyer_registration.html', {"form": form})


def post_request(request):    
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if  form.is_valid():
            request = form.save(commit=False)
            request.save()
            name = request.business_name
            email = request.business_email
            send_notification_email(name, email)           
            HttpResponseRedirect('home')
            return redirect('home')
  
    else:
        
        form =RequestForm()
 
    return render(request, 'request_form.html',{'form':form})


@require_POST
def cart_add(request, item_id):
    cart = Cart(request)  # create a new cart object passing it the request object 
    item = get_object_or_404(Item, id=item_id) 
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(item=item, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('home')


def cart_remove(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    cart.remove(item)
    return redirect('cart_detail',item_id)


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart_detail.html', {'cart': cart})
