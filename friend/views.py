from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from .models import FriendRequest, FriendList, Profile, Relationship, Messages
from  django.contrib.auth.models import User

def SendFriendRequest(request, receiver):
    r = User.objects.get(username = receiver)
    print(r)
    sender = Profile.objects.get(user = request.user)
    receiver_ = Profile.objects.get(user = r)
    status = "send"

    if Relationship.objects.filter(senderFriend = sender, receiverFriend = receiver_):
        return render(request, "Recommendation/friends.html", {"errMsg": "Friend request is already sent"})
    if Relationship.objects.filter(senderFriend = receiver_, receiverFriend = sender):
        return render(request, "Recommendation/friends.html", {"errMsg": "Friend request is already sent"})

    Relationship.objects.create(
        senderFriend = sender,
        receiverFriend = receiver_,
        status = status
    )

    #rel = Relationship(senderFriend = Profile.objects.get(user=sender), reciverFriend= Profile.objects.get(user=receiver_), status=status)
    #rel.save()

    return render(request, "Recommendation/friends.html")
def GetAllFriendRequests(request):
    user = Profile.objects.get(user = request.user)
    frndRequests = Relationship.objects.filter(receiverFriend = user, status="send")

    return  render(request, "Recommendation/friends.html", {"frdrequests": frndRequests})
def GetAllFriends(request):
    frnds =  Profile.objects.get(user=request.user)
    frndList = frnds.myFriends.all()
    print(frndList)
    msgNumbers=[]
    for frnd in frndList:
        sender = Profile.objects.get(user=frnd)
        msgs= Messages.objects.filter(messageSender=sender, messageReceiver=frnds, msgStatus="unread")
        no = msgs.count()
        msgNumbers.append(
            {
                'frnd' : frnd,
                'no' : no
            }
        )
    return render(request, "Recommendation/friends.html", {"frnds": msgNumbers})
def AcceptRequest(request, receiver):
    sender = User.objects.get(username=receiver)
    r = Profile.objects.get(user=request.user)
    s = Profile.objects.get(user=sender)
    obj = Relationship.objects.get(senderFriend=s, receiverFriend=r)
    if obj.status=="send":
        obj.status = "accepted"
    obj.save()
    return render(request, "Recommendation/friends.html")
def SendMessage(request):
    if request.method =="POST":
        receiver = request.POST.get("receiver")
        print(receiver)
        r = User.objects.get(username=receiver)
        sender = Profile.objects.get(user=request.user)
        receiver_ = Profile.objects.get(user=r)
        msg = request.POST['message']
        Messages.objects.create(
            messageSender = sender,
            messageReceiver = receiver_,
            messageValue = msg
        )
    messageObjects1 = Messages.objects.filter(messageSender=sender, messageReceiver=receiver_)
    messageObjects2 = Messages.objects.filter(messageSender=receiver_, messageReceiver=sender)
    messageObjects = messageObjects2.union(messageObjects1)

    return render(request, "Recommendation/SendMessage.html", {"msgs": messageObjects, "receiver": receiver})

def GoToSendMessage(request, receiver):
    r = User.objects.get(username=receiver)
    sender = Profile.objects.get(user=request.user)
    receiver_ = Profile.objects.get(user=r)
    print(sender)
    messageObjects1 = Messages.objects.filter(messageSender=sender, messageReceiver=receiver_)
    messageObjects2 = Messages.objects.filter(messageSender=receiver_, messageReceiver=sender)
    for msg in messageObjects2:
        msg.msgStatus="read"
        msg.save()
    messageObjects = messageObjects2.union(messageObjects1)

    return render(request, "Recommendation/SendMessage.html", {"msgs": messageObjects, "receiver": receiver})
    #return  render(request, "Recommendation/SendMessage.html", {"receiver": r})