from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from .models import *
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings

class Index(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        s=Product.objects.all()
        con={
            's':s
        }
        return Response (con) 

def search(request):
    search=Product.objects.all()
    con={'s':search}
    return render(request,'index.html',con)

class Shop(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'shop.html'
    def get(self, request, *args, **kwargs):
        p=Product.objects.all()
        c=Category.objects.all()
        cat=request.GET.get('cat')
        if cat:
            p=Product.objects.filter(category=cat)
        con={
            'p':p,'c':c
        }
        return Response (con) 
        

class CartList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'cart.html'
    def get(self, request, *args, **kwargs):
        carts=Cart.objects.filter(user=request.user,parchased=False)
        orders=Order.objects.filter(user=request.user,ordered=False)
        total_oroder=orders.count()
        if carts.exists() and orders.exists():
            
            order=orders[0]
            con={
                    'cart':carts,
                    'order':total_oroder
                } 
            return Response(con)         

class Contact(View):

    def get(self, request, *args, **kwargs):
        return render ( request,'contact.html')

class About(View):

    def get(self, request, *args, **kwargs):
        return render ( request,'about.html')

def Shop_Single(request,id):
    p=Product.objects.get(id=id)
    con={
        'p':p
    }
    return render ( request,'shop_single.html',con)


# class CartList(TemplateView):
#     template_name = 'cart.html'


def  add_cart(request,id):
   
    item=get_object_or_404(Product,id=id)
    order_item=Cart.objects.get_or_create(item=item,user=request.user,parchased=False)
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]      
        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity +=1
            order_item[0].save()
            messages.info(request,"Add the  product")
            return redirect('cart')
            

        else:
            order.orderitems.add(order_item[0])
            return redirect('cart')    

              
    else:
        order=Order(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        return redirect('/')

def  remove_cart(request,id):
    if request.user.is_authenticated:
        item=get_object_or_404(Product,id=id)
        order_qs=Order.objects.filter(user=request.user,ordered=False)
        if order_qs.exists():
            order=order_qs[0] 
            if order.orderitems.filter(item=item).exists():
                order_item=Cart.objects.filter(item=item,user=request.user,parchased=False)[0]
                order.orderitems.remove(order_item)
                order_item.delete()
                   
                return redirect("cart")
            else:
                  
                messages.info(request,"there is not product")
                return redirect("/")

        else:
            
            return HttpResponse('You have none')

# def contact(request):
#     if request.method=="POST":
        
#         # , from_email, to  'slalalal104@gmail.com', contact_email
#         # text_content = 'Thanks for yours email .you will get our answer'
#         # html_content = '<p>This is an <strong>important</strong> message.</p>'
#         send_mail(
#         subject,
#         mg,
#         "slalalal104@gmail.com",
#         [contact_email],
#         fail_silently=False,
# )
#     return render(request,'contact.html')    

def contact(request):
    if request.method == 'POST':
        contact_email=request.POST['email']
 
        subject= request.POST['subject'],
        message = request.POST['message']
        
        send_mail(
            subject,
            message,
         
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

    return render(request, 'contact.html')    