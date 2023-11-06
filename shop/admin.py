from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from django import forms
from .models import Category,Comment,Contact,Product,ProductImage,ProductSpecification,ProductSpecificationValue,ProductType
admin.site.register(Category,MPTTModelAdmin)

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification

class ProductImageInline(admin.TabularInline):
    model = ProductImage

class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
        ProductSpecificationValueInline,
    ]

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationInline,
    ]



































""" from .models import Category,Product,Character,Contact,Comment
# Register your models here.


class CharacterInline(admin.StackedInline):
    model = Character
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug',)
    prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('seller','slug','category','name','price',)
    inlines =[CharacterInline]
    save_as=True
    save_on_top=True
    prepopulated_fields = {'slug':('name',)}

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('product',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','product',) """

