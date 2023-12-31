from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager,PermissionsMixin)
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.core.mail import send_mail
import uuid



# Create your models here.

class CustomAccountmanager(BaseUserManager):
    def create_superuser(self,email,user_name,password,**other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_stuff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')
        return self.create_user(email,user_name,password,**other_fields)

    def create_user(self,email,user_name,password,**other_fields):
        if not email:
            raise ValueError(_('Youre must provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email,user_name=user_name,**other_fields)
        user.set_password(password)
        user.save()
        return user




class UserBase(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(_("email"),unique=True)
    user_name = models.CharField(max_length=250,unique=True)
    first_name = models.CharField(max_length=250,blank=True)
    last_name = models.CharField(max_length=250,blank=True)
    about = models.TextField(_("about"),max_length=500,blank=True)
    country = CountryField()
    phone = models.CharField(max_length=15,blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    object = CustomAccountmanager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'anton200705@gmail.com',
            [self.email],
            fail_silently=False,
        )


    def __str__(self) -> str:
        return self.user_name

class Address(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(UserBase,related_name='customer',verbose_name=_('Customer'),on_delete=models.CASCADE)
    full_name = models.CharField(_("Full Name"), max_length=150)
    phone = models.CharField(_("Phone Number"), max_length=50)
    postcode = models.CharField(_("Postcode"), max_length=50)
    address_line = models.CharField(_("Address Line 1"), max_length=255)
    address_line2 = models.CharField(_("Address Line 2"), max_length=255)
    town_city = models.CharField(_("Town/City/State"), max_length=150)
    delivery_instructions = models.CharField(_("Delivery Instructions"), max_length=255)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    default = models.BooleanField(_("Default"), default=False)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return "Address"