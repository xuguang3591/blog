import simplejson
import datetime
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.views import View
from user.views import authenticate
from post.models import Post, Content
from user.models import User
from utils import jsonify


class PostView(View):
    def get(self, request: HttpRequest):
        print('get ~~~~~~~~~~~~~')

    @authenticate
    def post(self, request: HttpRequest):
        post = Post()
        content = Content()
        try:
            payload = simplejson.loads(request.body)
            post.title = payload['title']
            post.author = User(id=request.user.id)
            post.postdate = datetime.datetime.now(
                datetime.timezone(datetime.timedelta(hours=8))
            )
            post.save()

            content.post = post
            content.content = payload['content']
            content.save()

            return JsonResponse({
                'post': jsonify(post, allow=['id', 'title'])
            }, status=200)

        except Exception as e:
            print(e)
            return HttpResponse(status=400)



@require_GET
def getpost(request: HttpRequest, id):
    print(id)
    return JsonResponse({}, status=201)
