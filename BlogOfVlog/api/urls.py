from django.urls import path
from . import views

urlpatterns = [
    path('',views.homepage , name='home'),
    path('blogpage/<str:pk>',views.blogpage,name='blogpage'),
    path('login/',views.loginpage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('signup/',views.signup,name='signup'),
    path('create-blog/',views.CreateBlog,name='create-blog'),
    path('update-blog/<str:pk>',views.UpdateBlog,name='update-blog'),
    path('delete-blog/<str:pk>',views.deleteBlog,name='delete-blog'),
    # path('check',views.CheckEmail,name='check'),
]