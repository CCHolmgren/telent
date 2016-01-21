from django.contrib import admin
from .models import Image, Profile, Profile, ImageReport, ImageLog, UserReport, Settings, Ban

# Register your models here.

def force_save_to_create_slug(modeladmin, request, queryset):
    for r in queryset.all():
        r.save()
force_save_to_create_slug.short_description = "Create a slug on marked Images"

class ImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'description', 'hidden')
    actions = [force_save_to_create_slug]

def mark_image_hidden(modeladmin, request, queryset):
    for r in queryset.all():
        r.image.hidden = True
        r.image.save()
        r.resolved = True
        r.save()

mark_image_hidden.short_description = "Mark reported image hidden"

class ImageReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'reason', 'resolved')
    actions = [mark_image_hidden]

class UserReportAdmin(admin.ModelAdmin):
    actions = []

def lift_account(modeladmin, request, queryset):
    queryset.delete()

class Ban_Admin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user']}),
        (None, {'fields': ['reason']})]

    list_display = ('user', 'reason')

    search_fields = ['user', 'reason']

    actions = [lift_account]

admin.site.register(Ban, Ban_Admin)

admin.site.register(Image, ImageAdmin)
admin.site.register(ImageReport, ImageReportAdmin)
admin.site.register(Profile)
admin.site.register(ImageLog)
admin.site.register(UserReport, UserReportAdmin)
admin.site.register(Settings)