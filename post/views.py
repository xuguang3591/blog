from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.views import View


class PostView(View):
    pass


def getpost(request: HttpRequest, id):
    print(id)

    return JsonResponse({}, status=201)
