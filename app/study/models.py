import os

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from rest_framework.exceptions import PermissionDenied

from .services import get_video_path, delete_old_video_path

User = get_user_model()


class Course(models.Model):
    teacher = models.ForeignKey(User,on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Проверяем, является ли пользователь учителем
        if self.teacher.is_teacher:
            super().save(*args, **kwargs)


class Subscription(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscriptions')
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')


class Lesson(models.Model):
    teacher = models.ForeignKey(User,on_delete=models.CASCADE, related_name='lessons')
    name = models.CharField(max_length=250)
    description = models.TextField()
    video = models.FileField(
        upload_to=get_video_path,
        validators=[FileExtensionValidator(allowed_extensions=['asf','mp4','flv','mkv'])],
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk:
            old_lesson = Lesson.objects.get(pk=self.pk)
            if old_lesson.video != self.video:
                old_file_path = old_lesson.video.path
                if old_file_path and os.path.exists(old_file_path):
                    os.remove(old_file_path)

        if self.teacher.is_teacher and self.course.teacher == self.teacher:
            super().save(*args, **kwargs)
        else:
            raise PermissionDenied("You are not allowed to create a lesson for this course.")


    def delete(self, *args, **kwargs):
        # Удаляем старый файл перед удалением объекта из базы данных
        if self.video:
            delete_old_video_path(self.video.path)
        # Вызываем стандартный метод delete для удаления объекта
        super().delete(*args, **kwargs)

