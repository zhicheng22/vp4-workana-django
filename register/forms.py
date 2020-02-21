from django import forms
from .models import *
from django.contrib.auth.models import User
import re

class UserForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', max_length=20, widget=forms.TextInput)
    last_name = forms.CharField(label='Last Name', max_length=20, widget=forms.TextInput)
    email = forms.EmailField(max_length=200)
    password = forms.CharField(label='Password', min_length=8, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', min_length=8, widget=forms.PasswordInput)
    username = forms.CharField(label='Username', max_length=20, widget=forms.TextInput, help_text=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] == cd['password2']:
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
            upper_number = 0
            special_number = 0
            for letter in list(cd['password']):
                if letter.isupper():
                    upper_number = upper_number + 1
                if regex.search(letter) != None:
                    special_number = special_number + 1

            if upper_number == 1 and special_number == 1:
                return cd['password2']
            else:
                raise forms.ValidationError('Passwords should contain a special character and a upper case letter')
        else:
            raise forms.ValidationError('Passwords do not match.')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'Please use another Username, that is already taken')
        return username

class BaseForm(forms.ModelForm):
    mobile_number = forms.CharField(label='Mobile Number', max_length=11, widget=forms.TextInput)
    zip_code = forms.CharField(label='Zip Code', max_length=4, widget=forms.TextInput)

    class Meta:
        model = BaseUser
        fields = ['mobile_number', 'house_number', 'street_address', 'subdivision', 'city', 'zip_code']

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        if len(mobile_number) == 11:
            try:
                number = int(mobile_number)
                return mobile_number
            except ValueError:
                raise forms.ValidationError('Mobile Number should contain only digits')
        else:
            raise forms.ValidationError('Mobile Number should be only 11 digits')

    def clean_zip_code(self):
        zip_code = self.cleaned_data['zip_code']
        if len(zip_code) == 4:
            try:
                number = int(zip_code)
                return zip_code
            except ValueError:
                raise forms.ValidationError('Zip Code should contain only digits')
        else:
            raise forms.ValidationError('Zip Code should be only 4 digits')




