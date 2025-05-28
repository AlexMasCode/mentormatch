from django.http import HttpResponse
from django.shortcuts import redirect

def _todo(_): return HttpResponse("TODO-сторінка ще не реалізована")

logout_view        = lambda r: (r.session.flush(), redirect("portal:login"))[1]
create_availability = _todo
mentor_reviews      = _todo
find_mentor         = _todo
give_feedback       = _todo
sessions            = _todo


def view_mentor_profile(request, mentor_id):
    return HttpResponse(f"<h1>Mentor profile page for ID {mentor_id}</h1>")