from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import  receiver
from .models import Profile, Relationship

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(post_save, sender= Relationship)
def post_save_add_to_friends(sender, created, instance, **kwargs):
    sender_ = instance.senderFriend
    receiver_ = instance.receiverFriend
    if instance.status=="accepted":
        sender_.myFriends.add(receiver_.user)
        receiver_.myFriends.add(sender_.user)
        sender_.save()
        receiver_.save()