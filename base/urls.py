from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name = 'home'),
    path('cart/',cart,name ='cart'),
    path('addcart/<int:pk>/',addcart,name = 'addcart'),
    path('remove/<int:pk>/',remove,name = 'remove'),
    path('plus/<int:pk>/',plus,name = 'plus'),
    path('minus/<int:pk>/',minus,name = 'minus'),
]