from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import OperatorProfile
from .models import Categ, Produs, Magazin

# Register your models here.

admin.site.register(Categ)
admin.site.register(Produs)
admin.site.register(Magazin)

class OperatorProfileInline(admin.StackedInline):
    model = OperatorProfile
    can_delete = False
    verbose_name_plural = 'Operator Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (OperatorProfileInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

