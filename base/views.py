from multiprocessing import context
from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,JsonResponse
from base.models import * 

from base.form import RoomForms,UserForm
from django.db.models import Q


from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from base.form import UserForm

from django.contrib import messages

from base.models import User


def namecheck(request):

    if request.method =="GET":
        name = request.GET.get('username')
        if User.objects.filter(username = name).exists():
            print(name)
            data ={
                'is_taken': True
            }
            return JsonResponse(data)
        else:
            print(name,'in the false block')
            data = {
                'is_taken': False
            }
            return JsonResponse(data)
@login_required()
def update_user(request):
    user = request.user
    form = UserForm(instance= user)


    context = {
        'form': form,

    }

    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile',pk=user.id)
    return render(request,'base/update_user.html',context)



def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    if request.method =='POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        

        try:
            user= User.objects.get(email=username)
        except:
            messages.error(request, 'the user is not registerd')
            return redirect('login')

        user = authenticate(request,email=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'password or  username is not correct')
            

    context = {
        "page": page,
    }
    return render(request,'base/login_register.html',context)



def logoutPage(request):

    logout(request)
    return redirect('home')



def registerPage(request):

    if request.user.is_authenticated:
        return redirect('home')

    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'error occurred while registering RETRY!')
            


    context = {
        'form': form,
    }
    return render(request,'base/login_register.html',context)




def home(request):

    profile = ''

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    

    rooms = Room.room.filter(Q(topic__name__icontains=q) | 
    Q(name__icontains = q) | 
    Q(description__icontains = q ) |
    Q(host__username__icontains = q)
     )

    room_count = rooms.count() 
    
    topics = Topic.objects.all()[0:4]

    # room_messages = Message.objects.all()
    # also need to set the messages based on the search functionality 

    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)|Q(user__username__icontains= q))


    
    context = {
        'rooms':rooms,
        'topics': topics,
        'room_count':room_count,
        'room_messages': room_messages,
        'profile': profile,
    }
    return render(request,'base/home.html',context)

# user Profile page

def userProfile(request,pk):
    
    profile = 'profile'
    
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_message = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user': user,
        'rooms': rooms,
        'topics': topics,
        'room_messages':room_message,
        'profile': profile,
    }
    return render(request,'base/profile.html',context)


def singleRoom(request,pk):

    single_room = Room.room.get(id = int(pk))
    room_messages = single_room.message_set.all().order_by('-created')
    participants = single_room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = single_room,
            body = request.POST.get('body')
        )
        single_room.participants.add(request.user)

        return redirect('roomDetail',pk = single_room.id)

    context = {
        'single_room':single_room,
        'room_messages': room_messages,
        'participants': participants
    }
    # print(room_messages,'❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️')

    return render(request,'base/room.html',context)

def delete_message(request,pk):

    message = Message.objects.get(id=pk)
    message.delete()
    pat = request.GET.get('pa')
    print(pat,'thiis the pathe of the previous paht of the browser hello jithin raj ndafjasdjflasdkjfasdjflasdkj444444444')
    
    return redirect(pat)

@login_required()
def createRoom(request):
    

    form = RoomForms()
    topics = Topic.objects.all()
    if request.method == 'POST':

        topic_from_form = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_from_form)

        Room.room.create(host=request.user,
        topic = topic,
        name = request.POST.get('name'),
        description = request.POST.get('description')
        )
        return redirect('home')

        # form = RoomForms(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        #     return redirect('home')

    
 
    context = { 
        'form': form,
        'redirect_field_name':'login',
        'topics':topics,
    }

    return render(request,'base/room_form.html',context)

@login_required()
def updateRoom(request,pk):
    update = True

    topics = Topic.objects.all()

    if Room.room.filter(host = request.user,id=pk).exists():
        singleRoom = Room.room.get(id=pk)
        form = RoomForms(instance=singleRoom)
        context = {
            'form':form,
            'topics':topics,
            'singleRoom': singleRoom,
            'update':update,
        }

        if request.method == "POST":
            topic_from_form  = request.POST.get('topic')
            topics,create = Topic.objects.get_or_create(name = topic_from_form) 
            singleRoom.name = request.POST.get('name')
            singleRoom.topic = topics
            singleRoom.description = request.POST.get('description')
            singleRoom.save()
            return redirect('home')


            
            return redirect('home')
    else:
        messages.error(request,'you cannot edit others room')
        return redirect('home')
    return render(request,'base/room_form.html',context)

# Create your views here.
@login_required()
def deleteRoom(request,pk):

    if Room.room.filter(host=request.user,id=pk).exists():

        singleroom = Room.room.get(id= pk)
        context = {
            'singleroom':singleroom
        }
        
        if request.method == 'POST':
            singleroom.delete()
            return redirect('home')
    else:
        messages.error(request,'you cannot delete others post')
        return redirect('home')
        
        # return redirect(request.META.get('HTTP_REFERER'))

    return render(request,'base/delete.html',context)

# moble resposive 

def topics(request):
    q = request.GET.get('topic') if request.GET.get('topic') != None else ''
    topic = Topic.objects.filter(name__icontains = q)
    context = {
        'topics': topic,
    }
    return render(request,'base/topics.html',context)

def activity(request):


    message = Message.objects.all()
    context = {
        'room_messages': message,

    }
    return render(request,'base/activity.html',context)

