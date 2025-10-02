from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Post(models.Model):
    description =models.TextField()
    title=models.CharField(max_length=500)
    author=models.CharField(max_length=200)
    date_posted=models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User,related_name='likes',blank=True)
    shares=models.ManyToManyField(User, related_name='shares',blank=True)
    
    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.count()
    
    def total_shares(self):
        return self.shares.count()

class Comment(models.Model):
    post=models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.author.username}-{self.content[:25]}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio=models.TextField()
    profile_pic = models.ImageField(upload_to='profile_pics/',blank=True,null=True)

    def __str__(self):
        return self.user.username

class Notifications(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='notifications')
    message=models.CharField(max_length=200)
    is_read=models.BooleanField(default=False)
    date_created=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Notification for {self.user.username}"
