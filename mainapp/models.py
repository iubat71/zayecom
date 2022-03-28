from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import DateTimeField
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class MainUser(AbstractUser):
    alluser=((1,'customer'),(2,'seller'))
    user_type=models.CharField(max_length=50,choices=alluser,default=2)
   


class Customer(models.Model):
    user=models.OneToOneField(MainUser,on_delete=models.CASCADE,primary_key=True)  
    password=models.CharField(max_length=50)
    USERNAME_FIELD='username'
    def __str__(self) :
        return self.user.username

class Seller(models.Model):
    user=models.OneToOneField(MainUser,on_delete=models.CASCADE,primary_key=True)
    password=models.CharField(max_length=50)

    USERNAME_FIELD='username'
    def __str__(self) :
        return self.user.username

@receiver(post_save,sender=MainUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            Customer.objects.create(user=instance)
        if instance.user_type==2:
            Seller.objects.create(user=instance)


@receiver(post_save,sender=MainUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.customer.save()
    if instance.user_type==2:
        instance.seller.save()


class Category(models.Model):
    name=models.CharField(max_length=50)
    time=DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return self.name

    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    
    name = models.CharField(max_length=255)

    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='product')
   
    price = models.DecimalField(max_digits=50, decimal_places=2)
    in_stock = models.PositiveIntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    
    def __str__(self) :
        return self.name
    class Meta:
        ordering=['-created']



class Cart(models.Model):
    user = models.ForeignKey(MainUser,on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)
    parchased=models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f'{self.item}x{self.quantity}'


    def get_total(self):
        total=self.item.price *self.quantity  
        f_total=format(total,'0.2f')
        return f_total



class Order(models.Model):
    orderitems = models.ManyToManyField(Cart)
    user=models.ForeignKey(MainUser,on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    payment_id=models.CharField(max_length=300,blank=True,null=True)
    orderid=models.CharField(max_length=300,blank=True,null=True)   
