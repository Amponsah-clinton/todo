from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    phone_number = forms.CharField(label='Phone Number', max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Profile.objects.create(user=user, phone_number=self.cleaned_data['phone_number'])
        return user
