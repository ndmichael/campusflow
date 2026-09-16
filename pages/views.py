from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


students = [
    {
        'id': 'std-001',
        'fullname': 'Lekan Olamilekan',
        'email': 'lekanl@gmail.com'
    },
    {
        'id': 'std-002',
        'fullname': 'Chiemerie Richard',
        'email': 'richard@gmail.com'
    },
    {
        'id': 'std-003',
        'fullname': 'Monturayo Ayomide',
        'email': 'ayomide@gmail.com'
    },
]

def home(request):
    context = {
        'students': students,
        "title": "aptechsys - home"
    }
    return render(request, "pages/index.html", context)

def about(request):
    context = {
        "title": "sys - about"
    }
    return render(request, "pages/about.html", context)

def contact(request):
    context = {
        "title": "sys - contact",
    }
    return render(request, "pages/contact.html", context)