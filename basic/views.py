from django.shortcuts import render
from .models import Posts,Room,Message
import secrets
from django.core.files.storage import FileSystemStorage
import string

from django.conf import settings
from django.core.mail import send_mail
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login as auth_login,logout
def index(request):
    
    return render(request,'index.html')

def login(request):
    
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect(index)

def login_submit(request):
    name=request.POST.get('name')
    pwd=request.POST.get('pwd')
    print(name,pwd)
    user=authenticate(request,username=name,password=pwd)
    if user is not None :
        auth_login(request, user)
        return render(request,'index.html')

    return render(request,'login.html',{'error':True})


def form_submit(request):
    title=request.POST.get('title')
    description=request.POST.get('description')
    tags=[request.POST.get('tags')]
    city=request.POST.get('city')
    country=request.POST.get('country')
    
    postedby=request.user.username
    for f in request.FILES:
        print('hello')
        print(f)
    post=Posts(Title=title,description=description,tags=tags,city=city,country=country,postedby=postedby)
    post.save()
    return render(request,'gift.html')

def gift_form(request):
    return render(request,'form.html')

def gift(request):
    posts=Posts.objects.filter(postedby=request.user.username)
    print(posts)
    data=[]
    for post in posts:
       if(len(post.requests)!=0):
            
         for i in post.requests:
            data.append(
                {
                    'title' : post.Title,
                    'postid' :post.id,
                    'requestedby' : i
                }
            )
    print("hello")
    print(data)
    return render(request,'gift.html',{'data':data})

def recieve(request):
    
    p=Posts.objects.all().exclude(postedby=request.user.username)
    #print(p[0].id)
    for post in p:
        print(post.Title)
    return render(request,'b-recieve.html',{'posts': p})

def req(request):
    postid=request.POST.get('postid')
    post=Posts.objects.get(id=postid)
    post.requests.append(request.user.username)
    post.save()
    print(post.requests)
    print('Request sent')
    p=Posts.objects.all().exclude(id=postid).exclude(postedby=request.user.username)
    return render(request,'b-recieve.html',{'posts': p})

def deny(request):
    x=request.POST.get('denied')
    x=x.split('|')
    print(x)
    postid=int(x[0])
    reqby=x[1]
    post=Posts.objects.get(id=postid)
    title=post.Title
    post.requests.remove(reqby)
    print(post.requests)
    post.save()
    subject="Request rejected :("
    message="Hello ! We are so sorry to say this, your request for the item "+title+" was rejected by the user."
    #########ADD EMAIL FUNCTION HERE
    u=User.objects.get(username=reqby)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [u.email ]
    send_mail( subject, message, email_from, recipient_list )
    print(reqby)
    return redirect(gift)


def accept(request):
    ########NOTIFY ACCEPTED
    ####notify other requesters
    x=request.POST.get('accepted')
    x=x.split('|')
    print(x)
    postid=int(x[0])
    reqby=x[1]
    p=Posts.objects.get(id=postid)
    title=p.Title
    p.requests.remove(reqby)
    p.save()
    usermail=User.objects.get(username=reqby).email

    subject = 'Request declined'
    message ='Hello! The item you requested '+title+' was given to another user :( Please try requestiong another item.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = []
    
    for u in p.requests:
                temp = User.objects.get(username=u)
                recipient_list.append(temp.email)
                print("denied"+temp.email)
    send_mail( subject, message, email_from, recipient_list )
    Posts.objects.filter(id=postid).delete()
    res = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
              for i in range(6))
    subject = 'Request Accepted !'
    message ='Hello! The request for the item '+title+' was accepted by the user :) Please check your inbox on Ginger Cake to connect with them.'
    email_from = settings.EMAIL_HOST_USER
    send_mail( subject, message, email_from, [usermail] )
    print("accept"+usermail)
    print("The generated random string : " + str(res))
    res=str(res)
    users=[]
    users.append(reqby)
    users.append(request.user.username)
    rooms=Room(code=res,users=users)
    rooms.save()
    msgval= request.user.username +" accepted "+reqby+"'s request for the item "+title
    msg=Message(value=msgval,user='Ginger Cake',room=res)
    msg.save()
    return redirect(gift)

def inbox(request):
    name=request.user.username
    room=Room.objects.all()
    data=[]
    for r in room:
        name=request.user.username
        print(r.users[0]+" "+r.users[1]+" "+name)
        if not(r.users[0]== name or r.users[1]==name):
            continue
        if r.users[0]==request.user.username:
            name=r.users[1]
            print(r.code)
    
        else : 
            name=r.users[0]
            print(r.code)
        data.append(
            {
                'code':r.code,
                'name':name
            }
        )
    print(data)
   
    return render(request,'b-inbox.html',{'data':data})

def checkview(request):
    room=request.POST['code']
    username=request.user.username
    return redirect('room/'+room)
    
def room(request,room):
    username=request.user.username
    roomid=Room.objects.get(code=room).code
    return render(request,'room.html',{
        'username' : username,
        'room' : room,
        'room_details' : roomid
    })

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    #room_details = Room.objects.get(code=room)
    print("Hello")
    messages = Message.objects.filter(room=room)
    #return HttpResponse('Message sent successfully')
    return JsonResponse({"messages":list(messages.values())})

def submit(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        #form.fields['postedby']=request.user.username
        if form.is_valid():
            #print(form.id)
            form.save()
            # Get the current instance object to display in the template
            #img_obj = form.instance
            post=Posts.objects.get(Title=request.POST.get('Title'))
            post.postedby=request.user.username
            post.save()
            return render(request, 'gift.html')
    else:
        form = PostForm()
    return render(request, 'index.html')