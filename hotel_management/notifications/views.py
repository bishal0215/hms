from django.http import HttpResponse


def index(request):
    return HttpResponse('Notifications app is ready. Use this area for real-time updates.')
