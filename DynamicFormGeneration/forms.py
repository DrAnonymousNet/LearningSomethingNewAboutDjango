from django import forms

# Form to create a Field Type
class FieldTypeForm(forms.Form):
    name = forms.CharField(label='Field Name')

# Form to create a Field for a Field
class FieldForm(forms.Form):
    field_name = forms.CharField(label='Field Name')
    field_type = forms.ChoiceField(choices=[
        ('text', 'Text'),
        ('file', 'File'),
        ('image', 'Image'),
        ('date', 'Date'),
        ('number', 'Number')
    ])

def generate_dynamic_form(Field_type):
    """
    Dynamically generate a form class based on the user-defined Field type.
    """
    class DynamicFieldForm(forms.Form):
        pass

    # Add fields to the form dynamically
    for field in Field_type.fields.all():
        if field.field_type == 'text':
            DynamicFieldForm.base_fields[field.field_name] = forms.CharField()
        elif field.field_type == 'file':
            DynamicFieldForm.base_fields[field.field_name] = forms.FileField()
        elif field.field_type == 'image':
            DynamicFieldForm.base_fields[field.field_name] = forms.ImageField()
        elif field.field_type == 'date':
            DynamicFieldForm.base_fields[field.field_name] = forms.DateField()
        elif field.field_type == 'number':
            DynamicFieldForm.base_fields[field.field_name] = forms.IntegerField()

    return DynamicFieldForm