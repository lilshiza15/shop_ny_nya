from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect,get_object_or_404
from .forms import RegistrationForm,UserEditForm,UserAddressForm
from.token import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .models import UserBase,Address
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from orders.views import user_orders
from django.urls import reverse
from shop.models import Product
from django.contrib import messages

# Create your views here.

@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request,'account/user/dashboard.html',{'orders':orders})

@login_required
def edit_details(request):
    if request.method=='POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        print(user_form.is_valid())
        if  user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request,'account/user/edit_details.html',{'user_form':user_form})

@login_required
def delete_user(request):
    user = UserBase.object.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirm')

def account_register(request):
    if request.user.is_authenticated:
        return redirect('account:dashboard')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('account/registration/account_activation_email.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            user.email_user(subject=subject,message=message)
            return HttpResponse('registered succesfully and activation sent')
    else:
        form = RegistrationForm()
    return render(request,'account/registration/register.html',{'form':form})

def account_activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.object.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')

@login_required
def view_address(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request,"account/dashboard/addresses.html",{"addresses":addresses})

@login_required
def add_address(request):
    if request.method=='POST':
        form = UserAddressForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return HttpResponseRedirect(reverse('account:addresses'))
    else:
        form = UserAddressForm()
    return render(request,'account/dashboard/edit_addresses.html',{'form':form})

@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, user=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address = Address.objects.get(pk=id, user=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})

@login_required
def delete_address(request, id):
    address = Address.objects.filter(pk=id, user=request.user).delete()
    return redirect("account:addresses")

@login_required
def set_default(request, id):
    Address.objects.filter(user=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, user=request.user).update(default=True)
    previous_url = request.META["HTTP_REFERER"]
    if 'delivery_address' in previous_url:
        return redirect('checkout:delivery_address')
    return redirect("account:addresses")   

@login_required
def wishlist(request):
    product = Product.objects.filter(user_wishlist=request.user)
    return render(request,'account/dashboard/user_wish_list.html',{"wishlist":product})

@login_required
def add_to__wishlist(request,id):
    product = get_object_or_404(Product,id=id)
    if product.user_wishlist.filter(id=request.user.id).exists():
        product.user_wishlist.remove(request.user)
        messages.success(request, product.title + " has been removed from your WishList")
    else:
        product.user_wishlist.add(request.user)
        messages.success(request,"Added "+ product.title +" to your wish list")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])



