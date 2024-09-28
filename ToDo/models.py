from django.db import models

# Create your models here.
class User(models.Model):
    first_name=models.CharField(max_length=255)
    middle_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.EmailField()
    password=models.CharField(max_length=255)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now=True)

def __str__(self):
    return f"{self.name}"


class Task(models.Model):
    User_id=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    name=models.CharField(max_length=255)
    completed=models.BooleanField(default=False)

def __str__(self):
    return f"{self.name}"