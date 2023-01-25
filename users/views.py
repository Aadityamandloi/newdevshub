from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Message
from django.db.models import Q
from .utils import searchProfiles, paginateProfiles
from .forms import CustomUserCreationForm, SkillForm, MessageForm,  ProfileForm
from django.contrib.auth.decorators import login_required
import requests
# from .models import  Profile
# Create your views here.
# loginUser to get user logged in and validate user authentication
def loginUser(request):
    page ='login'
    context = {'page':page}
    if request.user.is_authenticated :
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            # check in the database if the usernamme exists
            user = User.objects.get(username=username)
        except:
            messages.error(request,"Username does not exists")

        user = authenticate(request, username=username, password=password)
        
#         So what the login function is going to do is this will create a session for this user in the database.
# So in that sessions table, then it's also going to get that session and it's going to add that into
# our browsers cookies.
# So this is what officially sets that in the browser.
# And that's how we know a user is logged in and how they can have their permissions.
        if user is not None :
            login(request,user)
        #    So if a user successfully logs in, let's go ahead and redirect the user.
            return redirect('profiles')
        else:
            messages.error(request,"Username OR password is wrong")


    return render(request, 'users/login_register.html',context)
# end of loginUser 

# logout User to allow user logout 
def logoutUser(request):
    logout(request)
    messages.info(request,"User is logged out")
    return redirect('login')


def registerUser(request):
    page ='register'
    form =CustomUserCreationForm()

    if request.method == 'POST':
        form =CustomUserCreationForm(request.POST)
        if form.is_valid():
            user =form.save(commit=False)
            user.username =user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')
            
            login(request,user)
            return redirect('account')
        
        else:
            messages.error(request, 'An error has occured during registration!')


    context = {'page':page, 'form':form}
    return render(request, 'users/login_register.html',context)

def profiles(request):
    profiles, search_query =searchProfiles(request)
    custom_range, profiles =paginateProfiles(request, profiles, 3)
    #profiles =Profile.objects.all()

    # response= requests.get('http://127.0.0.1:8000/api/profile')    
    # data= response.json()

    context = {'profiles': profiles, 'search_query': search_query,
               'custom_range': custom_range}
   
    return render(request, 'users/profiles.html',context)


def userProfile(request,pk):
    profile=Profile.objects.get(id=pk)
    topskills = profile.skill_set.exclude(description__exact ="")
    otherskills = profile.skill_set.filter(description="")
    context ={'profile': profile,'topSkill': topskills,'otherSkill':otherskills}
    return render(request,'users/user-profile.html',context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context ={'profile':profile,'skills':skills,'projects':projects}
    return render(request,'users/account.html',context)


@login_required(login_url='login')
def editAccount(request):
    profile =request.user.profile
    form =ProfileForm(instance=profile)
    if request.method == 'POST':
        form=ProfileForm(request.POST,request.FILES,instance =profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context ={'form':form}
    return render(request,'users/profile_form.html',context)

@login_required(login_url='login')
def viewMessage(request,pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False :
        message.is_read = True
        message.save()

    context = {'message':message}
    return render(request, 'users/message.html', context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form =SkillForm()
    if request.method=='POST':
        form =SkillForm(request.POST)
        if form.is_valid():
            skill =form.save(commit=False)
            skill.owner=profile
            skill.save()
            messages.success(request, 'Skill was created successfully!')
            return redirect('account')
    context ={'form':form}
    return render(request,'users/skill_form.html',context)


@login_required(login_url='login')
def updateSkill(request,pk):
    profile = request.user.profile
    skill=profile.skill_set.get(id=pk)
    form =SkillForm(instance =skill)
    if request.method=='POST':
        form =SkillForm(request.POST,instance=skill)
        if form.is_valid():
            
            form.save()
            messages.success(request, 'Skill was updated successfully!')
            return redirect('account')
    context ={'form':form}
    return render(request,'users/skill_form.html',context)


def deleteSkill(request,pk):
    profile = request.user.profile
    skill=profile.skill_set.get(id=pk)
    if request.method =='POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('account')
    context={'object':skill}
    return render (request,'users/delete_template.html',context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST' :
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient


            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message has been sent successfully!')
            return redirect('user-profile',pk=recipient.id)

    context = {'recipient':recipient, 'form':form}
    return render(request, 'users/message_form.html', context)