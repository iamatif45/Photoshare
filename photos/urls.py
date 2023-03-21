from django.urls import path
from . import views



urlpatterns = [
    path('',views.gallery,name='Gallery'),
    path('photo/<str:pk>/',views.viewPhoto,name='photo'),
    path('add/',views.addPhoto,name='add'),
    path('login/',views.loginUser,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.registerUser,name='register'),
]
