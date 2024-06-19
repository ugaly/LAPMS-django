# from django.contrib import admin
# from .models import SystemUser


# admin.site.register(SystemUser)






# from django.contrib import admin

# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import SystemUser, ChatGroup

# # admin.site.register(SystemUser)



# class SystemUserAdmin(UserAdmin):
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {'fields': ('is_admin', 'is_citizen', 'is_landvaluer', 'is_landofficer', 'phone_number', 'full_name', 'thumbnail')}),
#     )
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         (None, {'fields': ('is_admin', 'is_citizen', 'is_landvaluer', 'is_landofficer', 'phone_number', 'full_name', 'thumbnail')}),
#     )

# from django import forms


# class GroupAdminForm(forms.ModelForm):
#     class Meta:
#         model = ChatGroup
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super(GroupAdminForm, self).__init__(*args, **kwargs)
#         self.fields['members'].queryset = SystemUser.objects.filter(is_landvaluer=True) | SystemUser.objects.filter(is_citizen=True)

# class GroupAdmin(admin.ModelAdmin):
#     form = GroupAdminForm
#     filter_horizontal = ('members',)

#     def save_model(self, request, obj, form, change):
#         super().save_model(request, obj, form, change)
#         print('AAAAAAAAAAAAAAAAAAAA', form.cleaned_data['members'])  # Debugging line

#     def save_related(self, request, form, formsets, change):
#         super().save_related(request, form, formsets, change)
#         obj = form.instance
#         print('BBBBBBBBBBBBBBBBBBBB', form.cleaned_data['members'])  # Debugging line
        
#         # Check if no members are selected
#         if not form.cleaned_data['members']:
#             # Get all land valuers
#             landvaluers = SystemUser.objects.filter(is_landvaluer=True)
#             print('CCCCCCCCCCCCCCCCCCCC', landvaluers)  # Debugging line
#             # Add all land valuers to the group
#             obj.members.set(landvaluers)

# admin.site.register(SystemUser)
# admin.site.register(ChatGroup, GroupAdmin)





from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SystemUser, ChatGroup, Message, Shapefile
from django import forms


class SystemUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_admin', 'is_citizen', 'is_landvaluer', 'is_landofficer', 'phone_number', 'full_name', 'thumbnail')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_admin', 'is_citizen', 'is_landvaluer', 'is_landofficer', 'phone_number', 'full_name', 'thumbnail')}),
    )

class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        self.fields['members'].queryset = SystemUser.objects.filter(is_landvaluer=True) | SystemUser.objects.filter(is_citizen=True)

class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    filter_horizontal = ('members',)
    list_display = ('id', 'name')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        print('AAAAAAAAAAAAAAAAAAAA', form.cleaned_data['members'])  # Debugging line

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.instance
        print('BBBBBBBBBBBBBBBBBBBB', form.cleaned_data['members'])  # Debugging line
        
        # Check if no members are selected
        if not form.cleaned_data['members']:
            # Get all land valuers
            landvaluers = SystemUser.objects.filter(is_landvaluer=True)
            print('CCCCCCCCCCCCCCCCCCCC', landvaluers)  # Debugging line
            # Add all land valuers to the group
            obj.members.set(landvaluers)

admin.site.register(SystemUser, SystemUserAdmin)
admin.site.register(ChatGroup, GroupAdmin)



class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat_group', 'sender', 'timestamp')
    search_fields = ('chat_group__name', 'sender__username', 'text')

admin.site.register(Message, MessageAdmin)
# admin.site.register(SystemUser)
# admin.site.register(ChatGroup, GroupAdmin)


# @admin.register(Shapefile)
# class ShapefileAdmin(admin.ModelAdmin):
#     list_display = ('name', 'uploaded_at')