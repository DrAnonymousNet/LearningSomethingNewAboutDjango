from django.db import models

# Model to store user-defined Field types and their fields
class FieldType(models.Model):
    name = models.CharField(max_length=255)  # Name of the form (e.g., 'User Submission Form')

# Model to store the fields (user-defined) for each Field
class FieldField(models.Model):
    FIELD_TYPES = [
        ('text', 'Text'),
        ('file', 'File'),
        ('image', 'Image'),
        ('date', 'Date'),
        ('number', 'Number'),
    ]
    Field_type = models.ForeignKey(FieldType, related_name='fields', on_delete=models.CASCADE)
    field_name = models.CharField(max_length=255)  # Field label (e.g., 'Title', 'Upload file')
    field_type = models.CharField(max_length=50, choices=FIELD_TYPES)

# Model to store the actual submissions based on the Field
class FieldSubmission(models.Model):
    Field_type = models.ForeignKey(FieldType, on_delete=models.CASCADE)
    submission_data = models.JSONField()  # To store the submitted data dynamically