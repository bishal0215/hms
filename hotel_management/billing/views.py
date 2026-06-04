from django.http import HttpResponse


def index(request):
    return HttpResponse('Billing app is ready. Use this area for invoices and payments.')
