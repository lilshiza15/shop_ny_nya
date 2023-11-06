from django.shortcuts import render,get_object_or_404
from .models import Category,Product,Comment
from django.views.generic import ListView,DetailView

# Create your views here.

""" class ProductListView(ListView):
    model = Product
    context_object_name = 'product_list'

    def get_queryset(self):
        return Product.product.get_queryset() """

def product_list(request):
    products = Product.objects.prefetch_related("product").filter(is_active=True)
    return render(request,'shop/product_list.html',{'product_list':products})
    


def product_detail(request,slug):
    product_detail = get_object_or_404(Product,slug=slug,is_active = True)
    return render(request,'shop/products/single_product.html',{'product':product_detail})
    
def category_detail(request,category_slug):
    category_detail = get_object_or_404(Category,slug=category_slug)
    product = Product.objects.filter(category__in=Category.objects.get(name=category_slug).get_descendants(include_self=True))
    return render(request,'shop/products/category.html',{'category':category_detail,'products':product})