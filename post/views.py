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
        try:
            page = int(request.GET.get('page', 1))
            page = page if page > 0 else 1
        except:
            page = 1
        try:
            size = int(request.GET.get('size', 20))
            size = size if size > 0 and size < 101 else 20
        except:
            size = 20
        try:
            start = (page - 1) * size
            posts = Post.objects.order_by('pk')[start:start + size]
            print(posts.query)

            return JsonResponse({
                'posts': [
                    jsonify(post, allow=['id', 'title'])
                    for post in posts
                ]
            })
        except Exception as e:
            print(e)
            return HttpResponse(status=400)

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
    try:
        id = int(id)
        post = Post.objects.get(pk=id)
        print(post)
        return JsonResponse({
            'post': {
                'id': post.id,
                'title': post.title,
                'author': post.author.name,
                'author_id': post.author_id,
                'postdate': post.postdate.timestamp(),
                'content': post.content.content
            }
        }, status=201)
    except Exception as e:
        print(e)
        return HttpResponse(status=404)
