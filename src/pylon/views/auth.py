from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user


@login_required
def require_login(request):
    user = get_user(request)
    user_data = {
        "username": user.username,
        "email": user.email,
        # You can add more user - related fields as needed
    }
    return JsonResponse(user_data)
