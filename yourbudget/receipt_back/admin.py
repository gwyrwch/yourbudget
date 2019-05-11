from django.contrib import admin

# Register your models here.
from receipt_back.models import User as Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Profile


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Profile


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm

    fieldsets = UserAdmin.fieldsets + (
        ('Extra fields', {'fields': ('date_of_birth', 'gender', 'city', 'country', 'telegram_username', 'fav_product')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra fields', {
            'classes': ('wide',),
            'fields': ('date_of_birth', 'gender', 'city', 'country', 'email', 'telegram_username', 'fav_product')
        }),
    )


admin.site.register(Profile, MyUserAdmin)
