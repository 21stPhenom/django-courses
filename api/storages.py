from django.utils.deconstruct import deconstructible

import cloudinary.uploader
from cloudinary_storage.storage import MediaCloudinaryStorage

@deconstructible
class CustomCloudinaryStorage(MediaCloudinaryStorage):

    def _upload(self, name, content):
        options = {'use_filename': True, 'resource_type': self._get_resource_type(name), 'tags': self.TAG}
        folder = "django_courses"
        options['folder'] = folder

        return cloudinary.uploader.upload(content, **options)

