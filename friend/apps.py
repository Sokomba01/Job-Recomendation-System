from django.apps import AppConfig


class FriendConfig(AppConfig):
    name = 'friend'
    def ready(self):
        import friend.signals
