from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from config.views import AppLogger

logger  = AppLogger(__name__)

@csrf_exempt
def login_user(request):
    template_name = "auth/login.html"

    if request.method == "GET":
        return render(request, template_name)

    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            info_message = f"User {username} #{user.id} has logged in"
            logger.info(info_message)
            return redirect(reverse("posts"))

        return render(request, template_name, {
            "error": "Invalid username or password"
        })

    return render(request, template_name)

def logout_user(request):
    info_message = f"User {request.user.username} #{request.user.id} has logged out"
    logger.info(info_message)
    logout(request)
    return redirect(reverse("login"))