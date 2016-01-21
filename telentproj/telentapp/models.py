from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from address.models import AddressField


# Create your models here.

class Settings(models.Model):
    allow_signup = models.BooleanField(default=True)

def upload_restaurantimage_to(instance, filename):
    import os
    from django.utils.timezone import now
    filename_base, filename_ext = os.path.splitext(filename)
    return '%s%s' % (
        now().strftime("%Y%m%d%H%M%S"),
        filename_ext.lower(),
    )


class AllNonHiddenObjects(models.Manager):
    def get_queryset(self):
        return super(AllNonHiddenObjects, self).get_queryset().filter(hidden=False, user__ban__isnull=True)


class Image(models.Model):
    user = models.ForeignKey(User, related_name="images")

    image = models.ImageField(upload_to=upload_restaurantimage_to)
    slug = models.SlugField()

    views = models.BigIntegerField(default=0)

    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    location = AddressField(blank=True, null=True)

    hidden = models.BooleanField(default=False)
    over_18 = models.BooleanField(default=False)

    all_objects = models.Manager()
    objects = AllNonHiddenObjects()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        from django.core import serializers
        log = ImageLog(user=self.user, action="Save", before_action=serializers.serialize("json", [self]))
        print(self.slug)
        if self.slug == '':
            import random
            self.slug = ''.join(
                    random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890") for _ in range(7))

        super(Image, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                update_fields=update_fields)
        log.after_action = serializers.serialize("json", [self])
        log.image_object = self
        log.save()

    def __str__(self):
        return "Image by {} ({})".format(self.user.username, self.get_absolute_url())

    def get_absolute_url(self):
        return reverse('image',
                       kwargs={'slug': self.slug})


class ImageLog(models.Model):
    user = models.ForeignKey(User)
    image_object = models.ForeignKey(Image)
    action_time = models.DateTimeField(auto_now_add=True)
    action = models.TextField()
    before_action = models.TextField(null=True)
    after_action = models.TextField(null=True)


class Profile(models.Model):
    user = models.OneToOneField(User)
    description = models.TextField(null=True, blank=True)
    profile_image = models.ForeignKey(Image, null=True)

    in_limbo = models.BooleanField(default=False)

    def __str__(self):
        return "Profile for {}".format(self.user.username)

    def get_absolute_url(self):
        return reverse('user_profile',
                       kwargs={'username': self.user.username})


class ImageReport(models.Model):
    image = models.ForeignKey(Image)
    user = models.ForeignKey(User)

    reason = models.TextField()
    resolved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserReport(models.Model):
    reported_user = models.ForeignKey(User)
    user = models.ForeignKey(User, related_name='user_reports')

    reason = models.TextField()
    resolved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Ban(models.Model):
    user = models.OneToOneField(User)
    reason = models.CharField(max_length=300)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

