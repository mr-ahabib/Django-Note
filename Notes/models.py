from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class UserProfile(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email


class Notes(models.Model):
    useremail = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(max_length=5000, null=True, blank=True)

    def __str__(self):
        return self.title if self.title else "Untitled Note"
