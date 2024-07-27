from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
app_name='polls'
urlpatterns = [
    path('',csrf_exempt(views.polls_controller),name='polls'),
    path("<int:pk>/",csrf_exempt(views.polls_manager), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("tags",csrf_exempt(views.tags_manager),name='tags'),
]
