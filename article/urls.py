from django.urls import path
from . import views

# start with article
urlpatterns = [
    # http://localhost:8000/article/
    path('', views.article_list, name='article_list'),
    path('<int:article_pk>', views.article_detail, name="article_detail"),
    path('type/<int:article_type_pk>', views.articles_with_type, name="articles_with_type"),
    path('date/<int:year>/<int:month>', views.articles_with_date, name="articles_with_date"),
]