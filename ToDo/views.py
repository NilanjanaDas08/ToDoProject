from django.shortcuts import render,redirect
from .models import Task,User
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password,make_password

# Create your views here.
def register(request):
   if request.method=="POST":
      first_name=request.POST.get('first_name')
      last_name=request.POST.get('last_name')
      email=request.POST.get('email')
      password=request.POST.get('password')
      if User.objects.filter(email=email).exists():
       print("Already exists")
       return HttpResponse("Already exists")
      else:
        hashed_password = make_password(password)
        user=User.objects.create(first_name=first_name,last_name=last_name,email=email,password=hashed_password)
        return redirect('login')
   return render(request,'register.html')
   
def login(request):
   config={}
   if 'user' in request.session:
      return redirect('task_list')
   if request.method=="POST":
      email=request.POST.get('email')
      password=request.POST.get('password')
      try:
       user=User.objects.get(email=email)
       if check_password(password,user.password):
         request.session['user']={
            'id':user.id,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email
 }
         print("Password is correct, redirecting to task_list")
         return redirect('task_list')
      except User.DoesNotExist:
       config['errors']='Invalid username or password'
   return render(request,'login.html',config)

   
def task_list(request):
    user_info=request.session['user']
    user_id=user_info['id']
    task=Task.objects.filter(user_id=user_id)
    if request.method=="POST":
        name=request.POST.get('name')
        if name:
           # Task.objects.create(name=name)
           Task.objects.filter(user__isnull=True).delete()
           if Task.objects.filter(name=name,user_id=user_id).count()>0: #Duplicate entry
             print("Already exists")
           else:
             Task.objects.create(name=name,user_id=user_id)
             return redirect('task_list')
    return render(request,'task_list.html',{'task':task},{'user_info':user_info})

def mark_as_done(request,task_id):
   task=Task.objects.get(id=task_id)
   task.completed=True
   task.save()
   return redirect('task_list')
 
def delete_task(request,task_id):
   task=Task.objects.get(id=task_id)
   task.delete()
   return redirect('task_list')