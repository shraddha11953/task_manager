from django.shortcuts import render

def homepage(request):
    return render(request, "index.html")

def register_page(request):
    return render(request, "register.html")

def tasks_page(request):
    return render(request, "tasks.html")
