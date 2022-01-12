from django.contrib import admin
from django.urls import path
from friend import views
urlpatterns = [
      path('myown/<receiver>',views.SendFriendRequest, name="myown"),
      path('frndrequests/',views.GetAllFriendRequests, name="frndrequests"),
      path('frnds/',views.GetAllFriends, name="frnds"),
      path('acceptReq/<receiver>',views.AcceptRequest, name="acceptReq"),
      path('sendMessage/',views.SendMessage, name="sendMessage"),
      path('GoToSendMsg/<receiver>',views.GoToSendMessage, name="GoToSendMsg")
]