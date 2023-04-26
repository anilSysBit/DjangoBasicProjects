from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
    
    def get_blog_count(self):
        return self.blog_set.count()
    

class Blog(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    description = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
    

class Review(models.Model):
    blog = models.ForeignKey(Blog,models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.body[:50]
    


