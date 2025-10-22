from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=20, null=False, blank=False)
    salary = models.IntegerField()

    class Meta:
        ordering = ('-salary',)

    def __str__(self):
        return self.user.first_name
