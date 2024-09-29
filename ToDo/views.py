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
    user_info = request.session['user']
    user_id = user_info['id']
    
    # Get the user instance using the user_id
    user_instance = User.objects.get(id=user_id)
    
    # Filter tasks using the user instance
    tasks = Task.objects.filter(user=user_instance)
    
    if request.method == "POST":
        name = request.POST.get('name')
        if name:
            # Check for duplicate tasks by name for the user instance
            if Task.objects.filter(name=name, user=user_instance).exists():  # Duplicate entry check
                print("Already exists")
            else:
                # Create a new task associated with the user instance
                Task.objects.create(name=name, user=user_instance)
                return redirect('task_list')
    
    return render(request, 'task_list.html', {'tasks': tasks, 'user_info': user_info})


   
'''def task_list(request):
    user_info=request.session['user']
    user_id=user_info['id']
    tasks=Task.objects.filter(user_id=user_id)
    if request.method=="POST":
        name=request.POST.get('name')
        if name:
           # Task.objects.create(name=name)
           if Task.objects.filter(name=name,user_id=user_id).count()>0: #Duplicate entry
             print("Already exists")
           else:
             user_instance = User.objects.get(id=user_id)
             Task.objects.create(name=name,user=user_instance)
             return redirect('task_list')
    return render(request,'task_list.html',{'tasks':tasks,'user_info':user_info})'''

def mark_as_done(request,task_id):
   task=Task.objects.get(id=task_id)
   task.completed=True
   task.save()
   return redirect('task_list')
 
def delete_task(request,task_id):
   task=Task.objects.get(id=task_id)
   task.delete()
   return redirect('task_list')

def logout(request):
   try:
      del request.session['user']
   except:
      pass
   return redirect('login')
