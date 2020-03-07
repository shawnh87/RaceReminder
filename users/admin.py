from django.contrib import admin
from .models import State
from .models import Region
from .models import EventType
from .models import Zip
from .models import Profile


admin.site.register(Zip)
admin.site.register(State)
admin.site.register(Region)
admin.site.register(EventType)
admin.site.register(Profile)
