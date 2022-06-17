from django.contrib import admin
from .models import User as UserModel, UserProfile as UserProfileModel, Hobby

# admin.site.register(UserModel)
# admin.site.register(UserProfileModel)
admin.site.register(Hobby)

from django.contrib import admin
from user.models import User, UserProfile, Hobby

# 사용 방법은 TabulaInline과 StackedInline 모두 동일
# 둘 다 사용해보고 뭐가 좋은지 비교해보기
# class UserProfileInline(admin.TabulaInline):
class UserProfileInline(admin.StackedInline):
    model = UserProfile

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'hobby':
            kwargs['queryset'] = Hobby.objects.filter(id__lte=7)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class UserAdmin(admin.ModelAdmin):
    inlines = (
            UserProfileInline,
        )

admin.site.register(User, UserAdmin)