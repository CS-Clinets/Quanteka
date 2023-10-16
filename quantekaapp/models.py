from django.db import models

# Create your models here.

class ReportCategory(models.Model):
    name = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.pk}. {self.name}"

class Report(models.Model):
    report_id = models.CharField(max_length=2000)
    name = models.CharField(max_length=255)
    small_description = models.CharField(max_length=1000, null=True)
    description = models.TextField(blank=True)
    image = models.FileField(upload_to='reports')
    category = models.ManyToManyField(
        ReportCategory, 
        related_name='reports',
        blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk}. {self.name}" if self.name else "None"
