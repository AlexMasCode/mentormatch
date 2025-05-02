from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.conf import settings
from requests import JSONDecodeError

from .forms import RegisterForm, LoginForm
from utils.api import api_request

class RegisterView(View):
    def get(self, request):
        return render(request, 'portal/register.html', {'form': RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if not form.is_valid():
            return render(request, 'portal/register.html', {'form': form})

        # збираємо корисне навантаження для auth_service
        payload = {
            'first_name':   form.cleaned_data['first_name'],
            'last_name':    form.cleaned_data['last_name'],
            'email':        form.cleaned_data['email'],
            'password':     form.cleaned_data['password'],
            'role':         form.cleaned_data['role'],
        }
        if form.cleaned_data['role'] == 'MENTOR':
            payload.update({
                'company_id':  form.cleaned_data['company_id'],
                'access_key':  form.cleaned_data['access_key'],
            })

        resp = api_request(
            'POST',
            f"{settings.AUTH_SERVICE_URL}/auth/register/",
            request.session,
            json=payload
        )
        if resp.status_code == 201:
            messages.success(request, 'Успішна реєстрація, тепер увійдіть.')
            return redirect('portal:login')

        try:
            detail = resp.json().get('detail') or resp.json()
        except (JSONDecodeError, ValueError):
            # если не JSON, покажем текст ответа
            detail = resp.text or f"HTTP {resp.status_code}"

        messages.error(request, detail)
        return render(request, 'portal/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        return render(request, 'portal/login.html', {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, 'portal/login.html', {'form': form})

        resp = api_request(
            'POST',
            f"{settings.AUTH_SERVICE_URL}/auth/login/",
            request.session,
            json=form.cleaned_data
        )
        if resp.ok:
            data = resp.json()
            request.session['access']  = data['access']
            request.session['refresh'] = data['refresh']
            return redirect('portal:home')

        try:
            detail = resp.json().get('detail') or resp.json()
        except (JSONDecodeError, ValueError):
            detail = resp.text or f"HTTP {resp.status_code}"
        messages.error(request, detail)

        return render(request, 'portal/login.html', {'form': form})

class HomeView(View):
    def get(self, request):
        if 'access' not in request.session:
            return redirect('portal:login')
        return render(request, 'portal/home.html')