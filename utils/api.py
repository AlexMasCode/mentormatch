import requests
from django.conf import settings

def api_request(method, url, session, **kwargs):
    headers = kwargs.pop('headers', {})
    token = session.get('access')
    if token:
        headers['Authorization'] = f'Bearer {token}'
    resp = requests.request(method, url, headers=headers, **kwargs)

    if resp.status_code == 401 and session.get('refresh'):
        r = requests.post(
            f"{settings.AUTH_SERVICE_URL}/api/auth/token/refresh/",
            json={'refresh': session['refresh']}
        )
        if r.ok:
            session['access'] = r.json()['access']
            headers['Authorization'] = f"Bearer {session['access']}"
            resp = requests.request(method, url, headers=headers, **kwargs)
    return resp