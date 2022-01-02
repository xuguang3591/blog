# from django.shortcuts import render
import datetime
import bcrypt
from utils import jsonify
from django.http import HttpRequest, JsonResponse, HttpResponse
import simplejson
import logging
from .models import User
from django.conf import settings
import jwt

AUTH_EXPIRE = 8 * 60 * 60
AUTH_HEADER = "HTTP_JWT"


def get_token(user_id):
    return jwt.encode({
        'user_id': user_id,
        'exp': int(datetime.datetime.now().timestamp()) + AUTH_EXPIRE
    }, settings.SECRET_KEY)


def reg(request: HttpRequest):  # POST
    try:
        payload = simplejson.loads(request.body)
        email = payload['email']
        # 先查询是否email已经存在
        u = User.objects.filter(email=email).first()
        if u:
            return JsonResponse({'error': '该用户已存在'}, status=400)

        name = payload['name']
        password = payload['password'].encode()
        print(type(password))

        # 写入数据库
        user = User()
        user.email = email
        user.name = name
        user.password = bcrypt.hashpw(password, bcrypt.gensalt()).decode()
        # user.password = password

        print(user, '-----------------')

        user.save()  # save会自动事务提交
        print(user, '~~~~~~~~~~~~~~~')

        return JsonResponse({
            'token': get_token(user.id)
        }, status=201)
    except Exception as e:
        logging.error(e)
        return JsonResponse({'error': '用户输入错误'}, status=400)


def login(request: HttpRequest):
    try:
        payload = simplejson.loads(request.body)
        email = payload['email']
        password = payload['password'].encode()

        user = User.objects.get(email=email)
        # print(user)

        if bcrypt.checkpw(password, user.password.encode()):
            token = get_token(user.id)
            print(token)
            res = JsonResponse({
                'user': jsonify(user, exclude=['password']),
                'token': token
            })
            res.set_cookie('jwt', token)
            # print(res)
            return res
        else:
            return JsonResponse({'error': '用户名密码错误'}, status=400)
    except Exception as e:
        logging.error(e)
        return JsonResponse({'error': '用户名密码错误'}, status=400)


class BlogAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: HttpRequest):
        print(1, '-' * 30)  # process_request
        print(list(filter(lambda x: x.find('JWT') >= 0, request.META.keys())))

        header = request.META.get(AUTH_HEADER, '')
        if not header:
            return HttpResponse(status=401)

        response = self.get_response(request)

        print(2, '-' * 30)  # process_response
        return response


def authenticate(viewfunc):
    def wrapper(*args):
        *s, request = args
        header = request.META.get(AUTH_HEADER, '')
        print(header)
        # header = header.split('=')[-1]

        if not header:
            print('----------')
            return HttpResponse(status=401)
        try:
            payload = jwt.decode(
                header,
                settings.SECRET_KEY,
                algorithms=['HS256'],
                options={'verify_signature': True}
            )
            print(payload, type(payload))
        except Exception as e:
            return HttpResponse(status=401)
        print('-' * 30)
        user_id = payload.get('user_id', 0)
        if user_id == 0:
            return HttpResponse(status=401)
        try:
            user = User.objects.get(pk=user_id)

        except Exception as e:
            print(e)
            return HttpResponse(status=401)
        request.user = user
        res = viewfunc(*args)
        return res

    return wrapper


@authenticate
def test(request):
    print('view function =========================')
    print(request, type(request))
    return JsonResponse({'test': 'ok'}, status=200)
