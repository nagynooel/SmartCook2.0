from django.db import models
from django.contrib.auth.models import User

from django.templatetags.static import static

from cookbook.storage import OverwriteStorage

def rename_file(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{instance.user.id}.{ext}"
    return f"profile/{filename}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(default="profile/default.svg", upload_to=rename_file, storage=OverwriteStorage())
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=36)
    expiry = models.DateTimeField()
    used = models.BooleanField(default=False)