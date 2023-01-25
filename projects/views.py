from django.shortcuts import render,redirect
from django.http import HttpResponse
from  .models import Project, Tag
from .forms import ProjectForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .utils import searchProjects, paginateProjects
import requests

def projects(request):
    projects, search_query =searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 3)

   

#     response= requests.get('http://127.0.0.1:8000/api/projects/')
    response= requests.get('https://newdevshub-production.up.railway.app/api/projects/')
    data= response.json()
   
    


    context ={'data':data,'projects': projects, 'search_query':search_query, 'custom_range':custom_range}
    return render(request, 'projects/projects.html',context)


def project(request, pk):
    projectobj =Project.objects.get(id=pk)
    return render(request, 'projects/singal-project.html', {'project': projectobj})

@login_required(login_url="login")
def createProject(request):
    form = ProjectForm()
    profile = request.user.profile
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project =form.save(commit =False)
            project.owner = profile
            project.save()
            return redirect('account')
    context = {'form' : form}
    return render(request,'projects/project_form.html', context)

@login_required(login_url="login")
def updateProject(request,pk):
    profile= request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method =='POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form' : form}
    return render(request,'projects/project_form.html', context)

@login_required(login_url="login")
def deleteProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    context = {'object':project}
    return render(request, 'projects/delete_template.html', context)


def home(request):
    response= requests.get('http://127.0.0.1:8000/api/projects/')    
    data= response.json()
    return render(request,'projects/projects.html',{'data':data})
