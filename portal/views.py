from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.conf import settings
from requests import JSONDecodeError
from django.views.generic import TemplateView
import jwt
from utils.jwt import peek_jwt, decode_jwt_payload

from .forms import RegisterForm, LoginForm
from utils.api import api_request
import requests
import logging


logger = logging.getLogger(__name__)


class RegisterView(View):
    def get(self, request):
        return render(request, 'portal/register.html', {'form': RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)

        if not form.is_valid():
            return render(request, 'portal/register.html', {'form': form})

        # Надсилаємо дані до auth_service для реєстрації
        resp = api_request(
            'POST',
            f"{settings.AUTH_SERVICE_URL}/register/",
            request.session,
            json=form.cleaned_data
        )

        if resp.status_code == 201:
            messages.success(request, 'Успішна реєстрація.')

            # Якщо роль - MENTOR, автоматично логінимо
            if form.cleaned_data['role'] == 'MENTOR':
                login_resp = api_request(
                    'POST',
                    f"{settings.AUTH_SERVICE_URL}/login/",
                    request.session,
                    json={
                        'email': form.cleaned_data['email'],
                        'password': form.cleaned_data['password']
                    }
                )

                if login_resp.ok:
                    data = login_resp.json()
                    # Зберігаємо дані сесії
                    request.session['access'] = data['access']
                    request.session['refresh'] = data['refresh']

                    jwt_data = decode_jwt_payload(data['access'])
                    request.session['user_id'] = jwt_data.get('user_id')
                    request.session['user_first_name'] = jwt_data.get('first_name')
                    request.session['role'] = jwt_data.get('role')

                    # Додатково: company_id, який знадобиться для подальших кроків
                    request.session['mentor_company_id'] = form.cleaned_data['company_id']

                    return redirect('portal:mentor_fields')
                else:
                    messages.error(
                        request,
                        'Не вдалося автоматично увійти, будь ласка, увійдіть вручну.'
                    )
                    return redirect('portal:login')

            # Для mentee або якщо роль інша
            messages.info(request, 'Тепер увійдіть у систему.')
            return redirect('portal:login')

        # Якщо не 201 — показуємо помилку
        messages.error(request, 'Реєстрація не вдалася. Спробуйте ще раз.')
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
            f"{settings.AUTH_SERVICE_URL}/login/",
            request.session,
            json=form.cleaned_data
        )
        if resp.ok:
            data = resp.json()

            request.session['access'] = data['access']
            request.session['refresh'] = data['refresh']

            # Распарсим access-токен
            jwt_data = decode_jwt_payload(data['access'])

            # Сохраняем данные из токена
            request.session['role'] = jwt_data.get('role')
            request.session['user_first_name'] = jwt_data.get('first_name')

            # Редирект по роли
            if jwt_data.get('role') == 'MENTEE':
                return redirect('portal:mentee_home')
            elif jwt_data.get('role') == 'MENTOR':
                return redirect('portal:mentor_home')

            return redirect('portal:home')

        # Обработка ошибок
        try:
            detail = resp.json().get('detail') or resp.json()
        except (JSONDecodeError, ValueError):
            detail = resp.text or f"HTTP {resp.status_code}"
        messages.error(request, detail)

        return render(request, 'portal/login.html', {'form': form})


class HomeView(View):
    """
    Показываем панель с меню, зависящим от роли.
    Если сессия не содержит access – редирект на /login/
    """

    def get(self, request):
        access = request.session.get('access')
        if not access:
            return redirect('portal:login')

        payload = peek_jwt(access)
        notifications_url = "/api/notifications/"
        ctx = {
            "access": access,
            "role": payload.get("role", "MENTEE"),
            "first_name": payload.get("first_name", ""),
            # API‑endpoint нотификаций (notification‑service)
            "notifications_api_url": notifications_url
        }
        return render(request, "portal/home.html", ctx)


class MenteeHomeView(View):
    def get(self, request):
        context = {
            "first_name": request.session.get("user_first_name", "User"),
            "next_session": {
                "mentor_name": "Ivan Petrenko",
                "specialization": "Data Engineering",
                "date": "May 10, 2024",
                "join_url": "#"
            },
            "notifications": [
                {"message": "Welcome, Oleksii! Your registration was successful."}
            ],
            "feedback_requests": [
                {"full_name": "Olena Kovalenko", "profile_url": "#"},
                {"full_name": "Andrii Shevchenko", "profile_url": "#"},
                {"full_name": "Mariana Zhuk", "profile_url": "#"}
            ],
            "recommended_mentors": [],
            "notifications_api_url": f"{settings.NOTIFICATION_SERVICE_URL}/mark-all-as-read/",
            "access": request.session.get("access")
        }
        # ——— ПОДГРУЖАЕМ 4 РЕКОМЕНДУЕМЫХ МЕНТОРА ———
        try:
            resp = requests.get(
                f"{settings.PROFILE_SERVICE_URL}/mentors/",
                headers={"Authorization": f"Bearer {context['access']}"},
                timeout=5
            )

            print(f"[DEBUG] GET {resp.url} → {resp.status_code}")
            print(f"[DEBUG] BODY: {resp.text}")

            if resp.status_code == 200:
                data = resp.json().get("results", [])
                # оставляем только первые 4
                context["recommended_mentors"] = data[:4]
        except requests.RequestException:
            # в случае ошибки просто оставим пустой список
            context["recommended_mentors"] = []

        return render(request, "portal/home_mentee.html", context)


class MentorHomeView(View):
    def get(self, request):
        access = request.session.get('access')
        # если не залогинились — кидаем на логин
        if not access:
            return redirect('portal:login')

        # ——— ПОДГРУЖАЕМ УВЕДОМЛЕНИЯ МЕНТОРА ———
        notifications = []
        try:
            resp = requests.get(
                f"{settings.NOTIFICATION_SERVICE_URL}/",
                headers={"Authorization": f"Bearer {access}"},
                timeout=5
            )
            if resp.status_code == 200:
                # ожидаем, что сервис возвращает { results: [ { message: ... }, ... ] }
                notifications = resp.json().get("results", [])
        except requests.RequestException:
            notifications = []




        # тут можешь подцепить реальные нотификации, сессии и заявки через api_request
        context = {
            "mentor_name": request.session.get("user_first_name", "Mentor"),
            "notifications": notifications,
            "upcoming_sessions": [
                {
                    "mentee_name": "John Doe",
                    "date": "May 12, 2025",
                    "time": "14:00",
                    "status": "Confirmed",
                    "join_url": "#"
                },
                {
                    "mentee_name": "Jane Smith",
                    "date": "May 13, 2025",
                    "time": "10:00",
                    "status": "Pending",
                    "join_url": "#"
                },
            ],
            "pending_requests": [
                {
                    "mentee_name": "Bob Johnson",
                    "requested_at": "2025-05-01",
                    "detail_url": "#"
                },
            ],
            "notifications_api_url": f"{settings.NOTIFICATION_SERVICE_URL}/mark-all-as-read/",
            "access": access,
        }
        return render(request, 'portal/home_mentor.html', context)

class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect('portal:login')


# ----------  Меню ментора ----------
class CreateAvailabilityView(View):
    def get(self, request):
        return render(request, 'portal/create_availability.html')

    def post(self, request):
        # TODO: call Session‑service API
        messages.success(request, 'Збережено ✔')
        return redirect('portal:home')


class MentorReviewsView(View):
    def get(self, request):
        return render(request, 'portal/mentor_reviews.html')


# ----------  Меню менті ----------
class FindMentorView(View):
    def get(self, request):
        # fake results demo
        q = request.GET.get('q')
        demo = [{'first_name': 'Alice', 'last_name': 'Mentor', 'field': 'Python'}] if q else None
        return render(request, 'portal/find_mentor.html', {'results': demo})


class GiveFeedbackView(View):
    def get(self, request):
        return render(request, 'portal/give_feedback.html')

    def post(self, request):
        # TODO: POST to rating‑service
        messages.success(request, 'Дякуємо за відгук!')
        return redirect('portal:home')


# ----------  Спільне ----------
class SessionsView(View):
    def get(self, request):
        return render(request, 'portal/sessions.html')


class ProfileView(TemplateView):
    template_name = 'portal/profile.html'


class MentorFieldSelectionView(View):
    """
            Allow a newly registered mentor to select their fields
            based on the industry of the company they chose at registration.
            """

    def get(self, request):
        access = request.session.get('access')
        if not access:
            return redirect('portal:login')

        # 1) Извлекаем auth_user_id из токена
        jwt_data = decode_jwt_payload(access)
        auth_user_id = jwt_data.get('user_id')
        logger.debug("Decoded auth user_id: %s", auth_user_id)

        # 2) Запрашиваем свой MentorProfile, передавая токен
        profile_id = request.session.get('mentor_profile_id')
        if not profile_id:
            try:
                url_lookup = f"{settings.PROFILE_SERVICE_URL}/mentors/?user_id={auth_user_id}"
                logger.debug("Lookup mentor profile via %s", url_lookup)
                lookup_resp = requests.get(
                    url_lookup,
                    headers={"Authorization": f"Bearer {access}"},
                    timeout=5
                )
                lookup_resp.raise_for_status()
                results = lookup_resp.json().get("results", [])
                profile_id = results[0]["id"] if results else None
                request.session["mentor_profile_id"] = profile_id
                logger.debug("Resolved mentor_profile_id: %s", profile_id)
            except Exception as e:
                logger.error("Error fetching mentor profile: %s", e, exc_info=True)

        if not profile_id:
            messages.error(request, "Не найден ваш ментор-профиль.")
            return redirect("portal:home")

        # 3) Получаем профиль, чтобы узнать company → industry_id
        industry_id = None
        try:
            url_comp = f"{settings.COMPANY_SERVICE_URL}/{request.session.get('mentor_company_id')}/"
            logger.debug("Fetching company for industry from %s", url_comp)
            comp = requests.get(url_comp, timeout=5).json()
            industry_id = comp.get('industry', {}).get('id')
            logger.debug("Extracted industry_id: %s", industry_id)
        except Exception as e:
            logger.error("Error fetching company: %s", e, exc_info=True)

        # 4) GET всех полей и фильтрация
        fields = []
        try:
            url_fields = f"{settings.CATALOG_SERVICE_URL}/fields/"
            logger.debug("Fetching fields list from %s", url_fields)
            all_fields = requests.get(url_fields, timeout=5).json().get('results', [])
            logger.debug("Total fields fetched: %d", len(all_fields))

            if industry_id:
                fields = [f for f in all_fields if f.get('industry', {}).get('id') == industry_id]
                logger.debug("Filtered fields count: %d", len(fields))
            else:
                fields = all_fields
        except Exception as e:
            logger.error("Error fetching/filtering fields: %s", e, exc_info=True)
            messages.error(request, "Не удалось загрузить список полей.")

        logger.debug("Fields for selection: %s", fields)
        return render(request, 'portal/mentor_fields.html', {
            'fields': fields
        })


    def post(self, request):
        raw = request.POST.getlist('fields')
        logger.debug("Raw POST getlist('fields'): %r", raw)

        # 1) Приводим к int
        try:
            selected = [int(x) for x in raw]
        except ValueError:
            messages.error(request, "Некорректные идентификаторы полей.")
            return self.get(request)
        logger.debug("Converted selected IDs to ints: %r", selected)

        access     = request.session.get('access')
        profile_id = request.session.get('mentor_profile_id')
        if not (access and profile_id):
            messages.error(request, "Session expired—please log in again.")
            return redirect("portal:login")

        url_patch = f"{settings.PROFILE_SERVICE_URL}/mentors/{profile_id}/"
        logger.debug("Will PATCH %s with specializations_ids=%r", url_patch, selected)

        try:
            patch_resp = requests.patch(
                url_patch,
                headers={
                    "Authorization": f"Bearer {access}",
                    "Content-Type": "application/json",
                },
                json={"specializations_ids": selected},
                timeout=5
            )
            logger.debug("PATCH status: %s", patch_resp.status_code)
            # посмотрите, что возвращает сервис
            try:
                body = patch_resp.json()
                logger.debug("PATCH response JSON: %s", body)
            except ValueError:
                logger.debug("PATCH response text: %s", patch_resp.text)

            patch_resp.raise_for_status()

            messages.success(request, "Your fields have been saved. Please log in.")
            return redirect("portal:mentor_home")

        except requests.HTTPError as e:
            err = e.response.text if e.response is not None else str(e)
            logger.error("PATCH failed: %s", err, exc_info=True)
            messages.error(request, f"Error saving fields: {err}")

        except Exception as e:
            logger.error("Unexpected error: %s", e, exc_info=True)
            messages.error(request, "Service unavailable—try again later.")

        # если что-то пошло не так, показываем форму снова
        return self.get(request)
