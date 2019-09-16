from django.shortcuts import render
from basic_app.forms import UserForm , MessageForm
from django.contrib.auth.models import User
from basic_app.models import MessagesInfo
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)



'''
the home page
'''
def index(request):
    return render(request,'basic_app/index.html')


#user must be login for this use
@login_required
def user_logout(request):

    logout(request)
    return HttpResponseRedirect(reverse('index'))


'''
this method get the MessageForm fill from
template save it in the Model MessagesInfo
user must be login for this use
'''
@login_required()
def send_message(request):

    if request.method == "POST":
        msg_form = MessageForm(data = request.POST)
        if msg_form.is_valid():
            obj = msg_form.save(commit=False)
            obj.sender_msg = request.user
            obj.status = "unread"
            obj.save()
    msg_form = MessageForm()
    return render(request,'basic_app/write_msg.html',
                        {'msg_form':msg_form})



'''
register new user if user name alredy exist
the web page will write a message user alredy
exist.
when user register the method will save his
info to the UseProfileInfo model
'''
def register(request):

    registered = False
    if request.method == "POST":
        user_form = UserForm(data= request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True

        else:
            print(user_form.errors )
    else:
        user_form = UserForm()

    return render(request,'basic_app/regestration.html',
                    {'user_form':user_form,
                    'registered':registered})




'''
method that return specific message
by id. if the reciver ask for the
message, the message status will change.
'''
def message_page(request, message_id):
    user_self = request.user

    # get the message if the sender or the reciver
    # is the request owner
    messages_list =  MessagesInfo.objects.filter(
                        Q(id=message_id, sender_msg=user_self)
                        |Q(id=message_id,reciver_msg=user_self))

    # if the reciver is the one that ask for
    # the message, the status will be change to "was readedn"
    MessagesInfo.objects.filter(id=message_id,
        reciver_msg = user_self).update(status='was readedn')

    # dictionery for the template
    date_dict = {'msg_record':messages_list,}
    return render(request,"basic_app/message_page.html",context = date_dict)




'''
user that is a reciver or sender of
specific message can delete it.
this method get request for delete message
if the user that request to delete message
is the message reciver/sender the message will
delete.
'''
@login_required
def delete_message(request, message_id):

    user_self = request.user

    # get the message if the sender or the reciver
    # is the request owner
    messages_list =  MessagesInfo.objects.filter(
                        Q(id=message_id, sender_msg=user_self)
                        |Q(id=message_id,reciver_msg=user_self))
    if messages_list:
        MessagesInfo.objects.filter(id=message_id).delete()

    return render(request,'basic_app/index.html')



'''
method that return dictionery with recied messages
and sent messages.
if the read_or_unread = 1 return all messages (readedn and unread)
if the read_or_unread = 0 return unreadn messages

'''
def get_messeges(request, read_or_unread):

    user_self = request.user

    #get all messages
    if(read_or_unread == 1):
        try:
            messages_out_list = MessagesInfo.objects.filter(sender_msg=user_self)
        except:
            messages_out_list = {}
        # list of messages that the user recied
        try:
            messages_in_list = MessagesInfo.objects.filter(reciver_msg=user_self)
        except:
            messages_in_list = {}

        # dictionery for the template
        return {'access_record':messages_out_list,
                    'out_messages':messages_in_list,}

    # get all unread messages
    elif read_or_unread == 0:

        # list of messages that the user recied
        try:
            messages_out_list = MessagesInfo.objects.filter(sender_msg=user_self, status= "unread")
        except:
            messages_out_list = {}

        # dictionery for the template
        try:
            messages_in_list = MessagesInfo.objects.filter(reciver_msg=user_self, status= "unread")
        except:
            messages_in_list = {}
        # dictionery for the template
        return {'access_record':messages_out_list,
                    'out_messages':messages_in_list, }


'''
return all specific users messages
'''
@login_required
def my_messages(request):

    # dictionery for the template
    date_dict = get_messeges(request, 1)
    return render(request,"basic_app/my_unread_messages.html",context = date_dict)


'''
all specific users unreadn
messages
'''
@login_required
def my_unread_messages(request):

        # dictionery for the template
        date_dict = get_messeges(request, 0)
        return render(request,"basic_app/my_messages.html",context = date_dict)




def user_login(request):
    if request.method== 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # django's built-in system authentication
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            logger.warn("someone tried to login and failed")
            logger.warn("Username:  {}  Password:  {}".format(username,password))
        return HttpResponse("Invalid login details supplied!")
    else:
        return render(request,'basic_app/login.html',{})
