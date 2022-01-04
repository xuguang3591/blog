import math
import simplejson
import datetime
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.views import View
from user.views import authenticate
from post.models import Post, Content
from user.models import User
from utils import jsonify


def validate(d: dict, name: str, type_func, default, validate_func):
    try:
        ret = type_func(d.get(name, default))
        ret = validate_func(ret, default)
    except:
        ret = default
    return ret


class PostView(View):
    def get(self, request: HttpRequest):
        print('get ~~~~~~~~~~~~~')
        page = validate(request.GET, 'page', int, 1, lambda x, y: x if x > 0 else y)
        size = validate(request.GET, 'size', int, 20, lambda x, y: x if x > 0 and x < 101 else y)
        try:
            start = (page - 1) * size
            posts = Post.objects.order_by('pk')
            print(posts.query)
            total = posts.count()
            posts = posts[start:start + size]
            print(posts.query)

            return JsonResponse({
                'posts': [
                    jsonify(post, allow=['id', 'title'])
                    for post in posts
                ],
                'pagination': {
                    'page': page,
                    'size': size,
                    'total': total,
                    'pages': math.ceil(total / size)
                }
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
