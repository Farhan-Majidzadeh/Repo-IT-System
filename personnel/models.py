from django.db import models
from django.core.validators import MinLengthValidator

class Department(models.Model):
    code = models.CharField(max_length=20, unique=True, validators=[MinLengthValidator(3)])
    name = models.CharField(max_length=100)
    building = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.code} - {self.name}"

class Personnel(models.Model):
    personnel_code = models.CharField(max_length=20, unique=True, validators=[MinLengthValidator(3)])
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    entry_date = models.DateField()
    settlement_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.personnel_code} - {self.full_name}"

class PersonnelDepartment(models.Model):
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    entry_date = models.DateField()
    exit_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=True)
    class Meta:
        unique_together = ('personnel', 'department', 'entry_date')
    def __str__(self):
        return f"{self.personnel} -> {self.department}"


