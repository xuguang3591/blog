from django.urls import re_path
from .views import PostView, getpost

urlpatterns = [
    re_path('^$', PostView.as_view()),
    re_path('^(\d+)$', getpost),
]