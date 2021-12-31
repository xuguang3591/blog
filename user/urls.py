from django.urls import path
from .views import reg, login, test

urlpatterns = [
    path('', reg),
    path('login', login),
    path('test', test)
]