from storages.backends.s3boto import S3BotoStorage
from django.conf import settings

class MediaStorage(S3BotoStorage):
    location = settings.MEDIAFILES_LOCATION
