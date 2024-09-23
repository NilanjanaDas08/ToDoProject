from django.shortcuts import render,redirect
from .models import Task

# Create your views here.

def task_list(request):
    task=Task.objects.all()
    if request.method=="POST":
        name=request.POST.get('name')
        if name:
           # Task.objects.create(name=name)
            if Task.objects.filter(name=name).count()>0: #Duplicate entry
             print("Already exists")
            else:
             Task.objects.create(name=name)
             return redirect('task_list')
    return render(request,'task_list.html',{'task':task})

def mark_as_done(request,task_id):
   task=Task.objects.get(id=task_id)
   task.completed=True
   task.save()
   return redirect('task_list')
 
def delete_task(request,task_id):
   task=Task.objects.get(id=task_id)
   task.delete()
   return redirect('task_list')