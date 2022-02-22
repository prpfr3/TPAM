from django.apps import AppConfig

class mainmenuConfig(AppConfig):
    name = 'mainmenu'

    #Tells Django to import signals that are used to trigger profile creation from user creation
    def ready(self):
        import mainmenu.signals
