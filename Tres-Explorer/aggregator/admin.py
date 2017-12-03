from django.contrib import admin

# Register your models here.
from .models import Userfavorite
admin.site.register(Userfavorite)
from .models import Userclasstrack
admin.site.register(Userclasstrack)
from .models import Usercontent
admin.site.register(Usercontent)
from .models import Userreview
admin.site.register(Userreview)
from .models import Usercheckin
admin.site.register(Usercheckin)
from .models import Classentry
admin.site.register(Classentry)
from .models import Facebookfriend
admin.site.register(Facebookfriend)
from .models import Instructorentry
admin.site.register(Instructorentry)
from .models import Userprofile
admin.site.register(Userprofile)
from .models import Usertag
admin.site.register(Usertag)
from .models import Newsfeed
admin.site.register(Newsfeed)
from .models import Studioentry
admin.site.register(Studioentry)
