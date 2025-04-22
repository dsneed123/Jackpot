from django import forms
from .models import Bucket

class BucketForm(forms.ModelForm):
    class Meta:
        model = Bucket
        fields = ['name', 'percentage']

    def clean_percentage(self):
        percentage = self.cleaned_data['percentage']
        if percentage < 0 or percentage > 100:
            raise forms.ValidationError("Percentage must be between 0 and 100.")
        return percentage
