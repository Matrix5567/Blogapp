from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .validators import validate_phone_number , validate_image
from django.contrib.auth.hashers import make_password




class SignupForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=255,widget=forms.TextInput(attrs={'class': 'form-control',
                                                                              'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=255,widget=forms.TextInput(attrs={'class': 'form-control',
                                                                             'placeholder': 'Last Name'}))
    nickname = forms.CharField(max_length=255,widget=forms.TextInput(attrs={'class': 'form-control',
                                                                            'placeholder': 'Nickname'}))
    address = forms.CharField(max_length=255,widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Address'}))
    phone_number = forms.CharField(validators=[validate_phone_number],
                                   widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    image = forms.ImageField(validators=[validate_image],
                             widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2','email','first_name','last_name','nickname','address','phone_number','image']


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserEditForm(forms.ModelForm):
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput, required=False)
    phone_number = forms.IntegerField(validators=[validate_phone_number,])
    image = forms.ImageField(validators=[validate_image])
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2','email','first_name','last_name','nickname',
                  'address','phone_number','image')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2


    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password1']:
            user.password = make_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
