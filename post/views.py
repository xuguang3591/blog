from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.views import View
from user.views import authenticate


class PostView(View):
    def get(self, request: HttpRequest):
        print('get ~~~~~~~~~~~~~')

    @authenticate
    def post(self, request: HttpRequest):
        print('post +++++++++++')


@require_GET
def getpost(request: HttpRequest, id):
    print(id)
    return JsonResponse({}, status=201)
