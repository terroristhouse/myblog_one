from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name=''),
    path('index/',views.index,name='index/'),
    path('life/',views.life,name='life/'),
    path('article_detail-<int:sid>.html',views.article_detail,name='article_detail/'),
    path('about/',views.about,name='about/'),
    path('message/',views.message,name='message/'),
    # 爬虫类url
    path('crawl/nmsghgnv/',views.nmsghgnv,name='crawl/nmsghgnv/'),
    path('crawl/wangyi/',views.wangyi,name='crawl/wangyi/'),
    path('crawl/Poetry/',views.Poetry,name='crawl/Poetry/'),

]
