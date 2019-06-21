from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User  
from tinymce.models import HTMLField
from django.utils.encoding import python_2_unicode_compatible
from django.urls import reverse
from django.conf import settings
from decimal import Decimal



 


# Create your models here.
class Item(models.Model):
    item_name = models.CharField(max_length = 50)     
    profile = models.ForeignKey(User,on_delete=models.CASCADE)    
    upload_date = models.DateTimeField(auto_now_add=True)
    item_picture = models.ImageField(upload_to='profile')
    expiry_date = models.DateTimeField(auto_now_add=False)
    original_price = models.IntegerField()
    today_price = models.IntegerField()

     
   

    class Meta:
        ordering = ('upload_date',)
        index_together=(('id','profile'),)

    def save_image(self):
        self.save()
    
    @classmethod
    def update_price(cls, update):
        pass
    
    @classmethod
    def get_item_by_id(cls):
        item = Item.objects.filter(id).first()
        return item
    
    @classmethod
    def get_profile_items(cls, profile):
        items = Item.objects.filter(profile__pk = profile)
        return items
    
    @classmethod
    def get_all_items(cls):
        items = Item.objects.all()
        return items
        
    def get_absolute_url(self):
        return reverse('item_detail' , args=[self.id])

class Profile(models.Model):
    business_logo = models.ImageField(upload_to='profile/',blank=True)
    business_description = HTMLField()
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

 
class Buyer(models.Model):
    first_name = models.CharField(max_length =300)
    last_name = models.CharField(max_length =300)
    email = models.EmailField()
    password = models.CharField(max_length = 300, null=False)


class Request(models.Model):
    business_name = models.CharField(max_length =100)
    business_identification_number = models.CharField(max_length =100)
    prefered_username = models.CharField(max_length =100)
    business_phone_number = models.IntegerField ()
    business_email = models.EmailField()
    Business_address = models.CharField(max_length =100) 

    def __str__(self):
            return self.name

    def save_request(self):
            self.save()
        
    

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self,  item, quantity=1, update_quantity=False):
        item_id = str(item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {'quantity': 0, 'today_price': str(item.today_price)}
        if update_quantity:
            self.cart[item_id]['quantity'] = quantity
        else:
            self.cart[item_id]['quantity'] += quantity
        self.save()


    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self,  item):
        item_id = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def __iter__(self):
        item_ids = self.cart.keys()
        items = Item.objects.filter(id__in=item_ids)
        for  item in  items:
            self.cart[str(item.id)][' item'] =  item

        for item in self.cart.values():
            item['today_price'] = Decimal(item['today_price'])
            item['total_price'] = item['today_price'] * item['quantity']
    
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['today_price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
 


