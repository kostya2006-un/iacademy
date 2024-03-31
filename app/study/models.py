from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from .services import get_video_path


User = get_user_model()


class Course(models.Model):
    teacher = models.ForeignKey(User,on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.title


class Lesson(models.Model):
    teacher = models.ForeignKey(User,on_delete=models.CASCADE, related_name='lessons')
    name = models.CharField(max_length=250)
    description = models.TextField()
    video = models.FileField(
        upload_to=get_video_path,
        validators=[FileExtensionValidator(allowed_extensions=['asf','mp4','flv','mkv'])],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


