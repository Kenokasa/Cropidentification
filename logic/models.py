from django.db import models
from django.contrib.auth.models import User

class CropDisease(models.Model):
    name = models.CharField(max_length=200)
    scientific_name = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    symptoms = models.TextField()
    treatment = models.TextField()
    prevention = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='disease_thumbs/')

    def __str__(self):
        return self.name

class PlantScan(models.Model):
    SCAN_TYPES = (
        ('IMG', 'Image Upload'),
        ('CAM', 'Camera Capture'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='plant_scans/')
    scan_type = models.CharField(max_length=3, choices=SCAN_TYPES)
    result = models.ForeignKey(CropDisease, on_delete=models.SET_NULL, null=True)
    confidence = models.FloatField(null=True)
    scan_date = models.DateTimeField(auto_now_add=True)
    analyzed_data = models.JSONField(default=dict)

    def __str__(self):
        return f"Scan {self.id} - {self.get_scan_type_display()}"

class PlantPart(models.Model):
    name = models.CharField(max_length=100)
    model_identifier = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    common_diseases = models.ManyToManyField(CropDisease)
    mesh_file = models.FileField(upload_to='3d_parts/')

    def __str__(self):
        return self.name
# models.py
class SolidWorksFile(models.Model):
    name = models.CharField(max_length=255)
    original_file = models.FileField(upload_to='uploads/')
    converted_filename = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=10)