import os


def get_video_path(instance, filename):
    return f"video/user_{instance.teacher.id}/{filename}"


def delete_old_video_path(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)