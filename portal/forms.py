from django import forms

class RegisterForm(forms.Form):
    ROLE_CHOICES = [
        ('MENTEE', 'Mentee'),
        ('MENTOR', 'Mentor'),
    ]

    first_name  = forms.CharField(label='Ім’я', max_length=30)
    last_name   = forms.CharField(label='Прізвище', max_length=30)
    email       = forms.EmailField(label='Email')
    password    = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    role        = forms.ChoiceField(label='Роль', choices=ROLE_CHOICES)

    # Ці поля потрібні лише якщо вибрали MENTOR
    company_id  = forms.IntegerField(label='ID компанії', required=False)
    access_key  = forms.CharField(label='Access Key', max_length=100, required=False)

class LoginForm(forms.Form):
    email    = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
