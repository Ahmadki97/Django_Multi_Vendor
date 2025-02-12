from django import forms
from .models import Vendor
from accounts.validators import allowOnlyImagesValidator

class VendorForm(forms.ModelForm):
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allowOnlyImagesValidator])
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']