from django import forms
from .models import User, UserProfile
from .validators import allowOnlyImagesValidator



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        


class UserProfileForm(forms.ModelForm):
    profile_pic = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allowOnlyImagesValidator])
    cover_pic = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allowOnlyImagesValidator])
    latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'start typing...', 'required': 'required'}))
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'cover_pic', 'address', 'country', 'state', 'city', 'latitude', 'longitude', 'pin_code']

        # Also we can make fields readonly by using the init method like following:
        # def __init__(self, *args, **kwargs):
        #     super(UserProfileForm, self).__init__(*args, **kwargs)
        #     for field in self.fields:
        #         if field == 'latitude' or field == 'longitude':
        #             self.fields[field].widget.attrs['readonly'] =  'readonly' 