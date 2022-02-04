from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser





class User(AbstractUser):
    name = models.CharField(max_length= 100,null=True)
    email = models.EmailField(max_length=100,unique=True)
    bio  = models.TextField(max_length= 500,null = True)
    image = models.ImageField(null=True,default='avatar.svg')
    # avatar = models.ImageField(upload = 'images',default='avatar.jpbg')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Topic(models.Model):
    name = models.CharField(max_length= 200)
    def __str__(self):
        return self.name
    

class Room(models.Model):
    
    room = models.Manager() 
    
    host = models.ForeignKey(User, on_delete= models.SET_NULL,null=True)
    topic  = models.ForeignKey(Topic,on_delete= models.SET_NULL, null=True)
    

    name = models.CharField(max_length = 200)
    description = models.TextField(null = True, blank = True)
    participants = models.ManyToManyField(User,related_name= "participants_set",blank=True)
    updated = models.DateTimeField(auto_now = True)
    # this method is used to whenever we are updating the database that time is stored on updated field
    created = models.DateTimeField(auto_now_add=True)
    # this is store the date and time when the instance is cereated

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return str(self.name)

class Message(models.Model):

    user = models.ForeignKey(User,on_delete= models.CASCADE)
    room = models.ForeignKey(Room, on_delete= models.CASCADE)

    body = models.TextField()
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-updated','-created']
        
    
    def __str__(self):
        return self.body[0:50]
    


    





# Create your models here.
