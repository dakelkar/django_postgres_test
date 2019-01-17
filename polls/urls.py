from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # views detail
    path('<int:question_id>/', views.detail, name='detail'),
    #views result
    path('<int:question_id>/results', views.results, name='results'),
    #view votes
    path('<int:question_id>/vote', views.vote, name='vote'),
]