from django.http import HttpResponse


def index(request):
    return HttpResponse('Users app is ready. Use this area for authentication and role management.')
