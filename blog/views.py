from django.contrib.auth.forms import PasswordChangeForm
from django.http import request
from django.urls.base import reverse_lazy
import blog
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .models import Blog, Category, Comments
from .forms import SignupForm,CommentForm
from django.urls import reverse
from django.contrib import auth
# Create your views here.

def home(request):
    post=Blog.objects.all()
    status=request.user.is_authenticated
    cat=Category.objects.all()
    return render(request,'blog/home.html',{'post':post,'status':status,'cat':cat})

def add_post(request):
    user={}
    item=User.objects.all()
    cat=Category.objects.all()
    status=request.user.is_authenticated
    if request.method=='POST':
        data=request.POST
        cat=Category.objects.get(name=data['category'])
        image=request.FILES.get('image')
        Blog.objects.create(title=data['title'],category=cat, author=request.user,body=data['body'],image=image)
        return redirect(home)
    else:
        user=User.objects.get(pk=request.user.id)   
    return render(request,'blog/add_post.html',{'item':item,'user':user,'status':status,'cat':cat})

def register(request):
    cat=Category.objects.all()
    status=request.user.is_authenticated
    if request.method == 'POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form=SignupForm()    
    return render(request,'blog/register.html',{'cat':cat,'form':form,'status':status})

def logout(request):
    auth.logout(request)
    return redirect('home')


def login_user(request):
    cat=Category.objects.all()
    status=request.user.is_authenticated
    error_msg=""
    if request.method == 'POST':
        data=request.POST
        username=data['username']
        raw_password=data['password']
        user=authenticate(username=username,password=raw_password)
        if not user:
            error_msg="Login credentials are wrong"
        else:
            login(request,user)
            return redirect('home')
    
    return render(request,'blog/login.html',{'cat':cat,'error':error_msg,'status':status})   

def detail(request,pk):
    post=Blog.objects.get(pk=pk)
    cat=Category.objects.all()
    lstatus=False
    same=False
    current=User.objects.get(username=post.author)
    if current.id == request.user.id:
        same=True
    if  not post.likes.filter(id=request.user.id).exists():
      lstatus=True
    status=request.user.is_authenticated
    comment=Comments.objects.filter(post=post)
    return render(request,'blog/detail.html',{'same':same,'comment':comment,'lstatus':lstatus,'cat':cat,'post':post,'status':status})

def delete(request,pk):
    cat=Category.objects.all()
    status=request.user.is_authenticated
    if 'delete' in request.POST:
     print("Delte buttton is pressed")
     Blog.objects.get(pk=pk).delete()
     return redirect('home')
    else:
        if 'edit' in request.POST:
            post=Blog.objects.get(pk=pk)
            return render(request,'blog/edit.html',{'post':post,'status':status,'cat':cat})
    return redirect('home')

def edit(request,pk):
   if request.method=='POST':
       data=request.POST
       post=Blog.objects.get(pk=pk)
       post.title=data['title']
       post.body=data['body']
       post.category=Category.objects.get(name=data['category'])
       if request.FILES.get('image'):
           post.image=request.FILES.get('image')
       post.save()
       return redirect('home')


def add_category(request):
    cat=Category.objects.all()
    status=request.user.is_authenticated
    if request.method == 'POST':
        data=request.POST
        Category.objects.create(name=data['name'])
        return redirect('home')
    return render(request,'blog/add_category.html',{'cat':cat,'status':status})

def likes(request,pk):
    
    post=get_object_or_404(Blog,id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        
    return HttpResponseRedirect(reverse('detail',args=[str(pk)])) 

def catdetail(request,category):
    cat=Category.objects.all()
    status=request.user.is_authenticated
    blog=Blog.objects.filter(category__name=category)
    category=category
    return render(request,'blog/catdetail.html',{'cat_name':category,'status':status,'cat':cat,'item':blog})

def comment(request,pk):
    post=get_object_or_404(Blog,pk=pk)
    if request.method =='POST':
        data=request.POST
        ar=request.user
        print("this is the user************8")
        print(post.author)
        Comments.objects.create(post=post,body=data['body'],author=ar)

     
    return HttpResponseRedirect(reverse('detail',args=[str(pk)]))

def deleteComment(request,pk):
    com=Comments.objects.get(pk=pk)
    id=com.post.id
    Comments.objects.get(pk=pk).delete()
    return HttpResponseRedirect(reverse('detail',args=[str(id)]))

def editProfile(request,pk):
    cat=Category.objects.all()
    user=User.objects.get(pk=pk)
    status=request.user.is_authenticated
    if request.method=='POST':
        data=request.POST
        user.username=data['username']
        user.first_name=data['firstname']
        user.last_name=data['lastname']
        user.email=data['email']
        user.save()
        return HttpResponseRedirect(reverse('editprofile',args=str(pk)))
    return render(request,'blog/editprofile.html',{'cat':cat,'status':status})

class ChangePassword(PasswordChangeView):
    form_class=PasswordChangeForm
    success_url=reverse_lazy('home')


    def get_context_data(self,*args, **kwargs):
    
        context = super().get_context_data(**kwargs)
        context['status']=self.request.user.is_authenticated
        context['cat']=Category.objects.all()

        return context