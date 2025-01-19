from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt

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
            return redirect(reverse("posts"))

        print("not found")
        return render(request, template_name, {
            "error": "Invalid username or password"
        })

    return render(request, template_name)
