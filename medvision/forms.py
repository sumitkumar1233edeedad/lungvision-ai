from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField(
        label="Upload Chest X-ray",
        widget=forms.FileInput(attrs={
            "class": "form-control",
            "accept": "image/*"
        })
    )