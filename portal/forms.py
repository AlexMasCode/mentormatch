from django import forms

class RegisterForm(forms.Form):
    ROLE_CHOICES = [
        ('MENTEE', 'Mentee'),
        ('MENTOR', 'Mentor'),
    ]

    first_name  = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={
        'placeholder': 'Enter your first name'
    }))
    last_name   = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={
        'placeholder': 'Enter your last name'
    }))
    email       = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address'
    }))
    password    = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password'
    }))
    role        = forms.ChoiceField(label='', choices=ROLE_CHOICES, widget=forms.Select(attrs={
        'placeholder': 'Select your role'
    }))

    company_id  = forms.IntegerField(label='', required=False, widget=forms.NumberInput(attrs={
        'placeholder': 'Enter your Company'
    }))
    access_key  = forms.CharField(label='', max_length=100, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Secret Key'
    }))


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password'
    }))
