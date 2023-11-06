from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('products/',views.product_list,name='products'),
    path('products/<slug:slug>',views.product_detail,name="products_detail"),
    path('category/<slug:category_slug>',views.category_detail,name="category_detail"),
]

