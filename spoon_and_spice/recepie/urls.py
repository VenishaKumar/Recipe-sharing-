from django.urls import path
from . import views

urlpatterns = [
    
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('',views.home,name="home"),
    path('add_recepie',views.add_recepie,name="add_recepie"),
    path('search_dish',views.search_dish,name="search_dish"),
    
   path('category/<str:category_name>/', views.category_dishes, name='category_dishes'),  # For category
    path('cuisine/<str:cuisine_name>/', views.category_dishes, name='cuisine_dishes'),  # For cuisine
    path('general/<str:general_name>/', views.category_dishes, name='general_dishes'),

]