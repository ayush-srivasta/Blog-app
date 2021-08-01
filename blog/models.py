from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
import datetime
# Create your models here.


class Category(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title=models.CharField(max_length=200,blank=False)
    likes=models.ManyToManyField(User,related_name='like_post',blank=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='media/', blank=True,null=True)
    body=models.TextField()
    
    def __str__(self):
        return self.title

    def like_count(self):
        return self.likes.count() 

class Comments(models.Model):
   post=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='comments')
   body=models.TextField(blank=True,null=True)
   created_on=models.DateTimeField(auto_now_add=True )
   author=models.ForeignKey(User,on_delete=models.CASCADE ,null=True)
   def __str__(self):
       return self.body