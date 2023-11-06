from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey 
from django.utils.translation import gettext_lazy as _
from config.settings.base import AUTH_USER_MODEL
# Create your models here.

class Category(MPTTModel):
    name = models.CharField(verbose_name=_('Category name'),help_text=_('Required and unique'),max_length=150,unique=True)
    slug = models.SlugField(verbose_name=_('Category safe URL'),max_length=150,unique=True)
    parent = TreeForeignKey('self',related_name='children',null=True,on_delete=models.SET_NULL,blank=True)
    img = models.ImageField(upload_to='categories/',blank=True)
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def get_absolute_url(self):
        return reverse("shop:category_detail", kwargs={"category_slug": self.slug})
    

    def __str__(self):
        return self.name
    
class ProductType(models.Model):
    name = models.CharField(verbose_name=_('Product type'),help_text=_('Required'),max_length=150,unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Product type')
        verbose_name_plural = _('Product types')

    def __str__(self):
        return self.name

class ProductSpecification(models.Model):
    product_type = models.ForeignKey(ProductType,on_delete=models.RESTRICT) 
    name = models.CharField(verbose_name=_('Name'),help_text=_('Required'),max_length=150)

    class Meta:
        verbose_name = _('Product Specification')
        verbose_name_plural = _('ProductSpecifications')

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category,related_name='products',on_delete=models.SET_NULL,null=True)
    product_type = models.ForeignKey(ProductType,on_delete=models.RESTRICT) 
    title = models.CharField(verbose_name=_('Title'),help_text=_('Required'),max_length=150)
    slug = models.SlugField(max_length=200, db_index=True)
    #image = models.ForeignKey('ProductImage',related_name='product_image',on_delete=models.SET_DEFAULT)
    description = models.TextField(verbose_name=_('Description'),help_text=_('Not Required'),blank=True)
    regular_price = models.DecimalField(verbose_name=_('Regular price'),help_text=('Maximum 999999.9'),error_messages={
        "name":{
            "max_length":_('The price must be between 0 and 999999.9'),
        },
    },max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(verbose_name=_('Discount price'),help_text=('Maximum 999999.9'),error_messages={
        "name":{
            "max_length":_('The price must be between 0 and 999999.9'),
        },
    },max_digits=10, decimal_places=2)
    is_active = models.BooleanField(verbose_name=_('Product visibility'),help_text=_('Change product visibility'),default=True)
    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)
    user_wishlist = models.ManyToManyField(AUTH_USER_MODEL,related_name='wishlist',blank=True)
    

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse("shop:products_detail", kwargs={"slug": self.slug})
    

    def __str__(self):
        return self.title

class ProductSpecificationValue(models.Model):
    product = models.ForeignKey(Product,related_name='products',on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification,related_name='specification',on_delete=models.RESTRICT)
    value = models.CharField(verbose_name=_('Value'),help_text=_('Product Specification Value'),max_length=255)

    class Meta:
        verbose_name = _('Product Specification Value')
        verbose_name_plural = _('Product Specification Values')

    def __str__(self):
        return self.value

class ProductImage(models.Model):
    product = models.ForeignKey(Product,related_name='product',on_delete=models.CASCADE)
    image = models.ImageField(verbose_name = _("Image"),help_text=_('Upload a product image'), upload_to='products/%Y/%m/%d',default="products/default-image.jpg")
    alt_text = models.CharField(verbose_name=_('Alternative image text'),help_text=_('Please add alternative image text'),null=True,blank=True,max_length=250)
    is_feature = models.BooleanField(default=False)
    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True,editable=False)

    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')
    
class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    message = models.TextField(max_length=500) 
    product = models.ForeignKey(Product,related_name='comment',on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name