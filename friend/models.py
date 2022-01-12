from django.db import models
from  django.conf import settings
from django.db.models import ForeignKey
from  django.utils import timezone
from django.contrib.auth.models import User

class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friends")

    def __str__(self):
        return self.user.username
    def addFriend(self, account):
        if not account in self.friends.all():
            self.friends.add(account)


    def removeFriend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        removerFriendsList = self
        removerFriendsList.removeFriend(removee)
        friendsList = FriendList.objects.get(user=removee)
        friendsList.removeFriend(self.user)
    def isMutualFriend(self, friend):
        if friend in self.friends.all():
            return True
        return False

class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")
    isActive = models.BooleanField(blank=True, null=False, default=True)
    timeStamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username
    def accept(self):
        receiverFriendList = FriendList.objects.get(user=self.receiver)
        if receiverFriendList:
            receiverFriendList.addFriend(self.sender)
            senderFriendList = FriendList.objects.get(user=self.sender)
            if senderFriendList:
                senderFriendList.addFriend(self.receiver)
                self.isActive = False
                self.save()
    def decline(self):
        self.isActive = False
        self.save()
    def cancle(self):
        self.isActive = False
        self.save()
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    myFriends = models.ManyToManyField(User, related_name="myFriends", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    def get_friends(self):
        return self.myFriends.all()

    def get_friend_no(self):
        return self.myFriends.all().count()

STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted'),
)
class Relationship(models.Model):
    senderFriend: ForeignKey = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="senderFriend")
    receiverFriend = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="receiverFriend")
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.senderFriend}-{self.receiverFriend}-{self.status}"
class Messages(models.Model):
    messageSender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="messageSender")
    messageReceiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="messageReceiver")
    messageValue = models.CharField(max_length=1000, null=False)
    msgStatus = models.CharField(max_length=10, default="unread")
    created = models.DateTimeField(auto_now_add=True)