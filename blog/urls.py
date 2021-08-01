from django.contrib.auth import login
from django.urls import path,include
from .import views
urlpatterns = [

    path('',views.home,name='home'),
    path('addpost/',views.add_post,name='add_post'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('login',views.login_user,name='login'),
    path('detail/<int:pk>',views.detail,name='detail'),
    path('delete<int:pk>',views.delete,name='delete'),
    path('edit/<int:pk>',views.edit,name='edit'),
    path('add_category/',views.add_category,name='add_category'),
    path('likes/<int:pk>',views.likes,name='like'),
    path('category/<str:category>',views.catdetail,name='catdetail'),
    path('comments/<int:pk>',views.comment,name='comment'),
    path('deletecomment/<int:pk>',views.deleteComment,name='deleteComment'),
    path('editprofile/<int:pk>',views.editProfile,name='editprofile'),
    path('changepassword/',views.ChangePassword.as_view(template_name='blog/changepassword.html'),name='changepassword')
]
