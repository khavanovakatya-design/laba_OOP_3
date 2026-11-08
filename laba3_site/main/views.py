from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def p404(request):
    return render(request, '404.html')