from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'a user with that email already exists.')
        return email


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['age', 'address', 'number', 'name', 'photo',]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address'}),
        }


class ChangeSocialMediaForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    class Meta:
        model = CustomUser
        fields = ['website', 'instagram', 'gitHub', 'twitter', 'facebook']
        widgets = {
            'website': forms.TextInput(attrs={'placeholder': 'Website'}),
            'instagram': forms.TextInput(attrs={'placeholder': 'Instagram'}),
            'gitHub': forms.TextInput(attrs={'placeholder': 'Github'}),
            'twitter': forms.TextInput(attrs={'placeholder': 'Twitter'}),
            'facebook': forms.TextInput(attrs={'placeholder': 'facebook'}),
        }
