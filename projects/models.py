from django.db import models
from django.core.validators import MinLengthValidator

class Project(models.Model):
    code = models.CharField(max_length=20, unique=True, validators=[MinLengthValidator(3)])
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.code} - {self.name}"
