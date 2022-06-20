from tkinter import N
from django.contrib import admin
from .models import User as UserModel, UserProfile as UserProfileModel, Hobby as HobbyModel
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# 사용 방법은 TabulaInline과 StackedInline 모두 동일 스택은 세로 , 타불라는 가로 
# class UserProfileInline(admin.TabulaInline):
class UserProfileInline(admin.StackedInline):
    model = UserProfileModel

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'hobby':
            kwargs['queryset'] = HobbyModel.objects.filter(id__lte=7)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'fullname', 'email',) #보여주는 리스트
    list_display_links = ('username',) #상세로 들어가는 링크
    list_filter = ('username',)
    search_fields = ('username', 'email',)
    
    fieldsets = (
        ("info", {'fields': ('username', 'password', 'email', 'fullname', 'join_date',)}), 
        ('Permissions', {'fields': ('is_admin', 'is_active',)}),)
    
    filter_horizontal = []
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('username', 'join_date',)
        else:
            return ('join_date',)
        
    inlines = (
            UserProfileInline,
        )

admin.site.register(UserModel, UserAdmin)
admin.site.register(HobbyModel)