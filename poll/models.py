from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    title = models.TextField(null=False)
    is_active = models.BooleanField(default=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_ts = models.DateTimeField(auto_now_add=True)
    mod_ts = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(null=False)
    create_ts = models.DateTimeField(auto_now_add=True)
    mod_ts = models.DateField(auto_now=True)

    def __str__(self):
        return self.text
    