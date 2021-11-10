from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(AskingModel)
admin.site.register(Question)
admin.site.register(UserAnswers)
admin.site.register(UserAskings)
