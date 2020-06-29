from django.shortcuts import render, HttpResponse, redirect
from blog.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time, json, random


# Create your views here.
# 母版
def base(request):
    return render(request, 'base.html', locals())


# 首页
def index(request):
    article = Article.objects.all().order_by('-modified_time')[:100]
    article_head = Article.objects.all().order_by('-views')[:5]
    currentPage = int(request.GET.get('page', 1))  # 获取当前在第几页
    paginator = Paginator(article, 5)  # 告诉分页器我5条分页
    # 如果总页数大于十一页，设置分页
    if paginator.num_pages > 11:
        # 如果当前页数小于5页
        if currentPage - 5 < 1:
            # 页面上显示的页码
            pageRange = range(1, 11)
        # 如果当前页数+5大于总页数显示的页码
        elif currentPage + 5 > paginator.num_pages:
            pageRange = range(paginator.num_pages - 9, paginator.num_pages + 1)
        else:
            # 在中间显示的十个页码
            pageRange = range(currentPage - 5, currentPage + 5)
    else:
        pageRange = paginator.page_range
    # 捕获路由异常
    try:
        article = paginator.page(currentPage)
    # 如果页码输入不是整数则返回第一页的数据
    except PageNotAnInteger:
        article = paginator.page(1)
    # 如果页码输入是空值则返回第一页数据
    except EmptyPage:
        article = paginator.page(1)
    return render(request, 'index.html', locals())


# 生活笔记
def life(request):
    article = quote.objects.all().order_by('-ID')
    return render(request, 'life.html', locals())


# 网易新闻
def wangyi(request):
    content = '学的不仅是技术，更是梦想！！！学的不仅是技术，更是梦想！！！学的不仅是技术，更是梦想！！！学的不仅是技术，更是梦想！！！学的不仅是技术，更是梦想！！！学的不仅是技术，更是梦想！！！学的不仅是技术，更是梦想！！！学的不仅是技术，更是梦想！！！学的不仅是技术，更是梦想！！！学的不仅是技术，更是梦想！！！学的不仅是技术，更是梦想！！！学的不仅是技术，更是梦想！！！学的不仅是技术，更是梦想！！！学的不仅是技术，更是梦想！！！学的不仅是技术，更是梦想！！！学的不仅是技术，更是梦想！！！学的不仅是技术，更是梦想！！！学的不仅是技术，更是梦想！！！学的不仅是技术，更是梦想！！！学的不仅是技术，更是梦想！！！学的不仅是技术，更是梦想！！！学的不仅是技术，更是梦想！！！学的不仅是技术，更是梦想！！！学的不仅是技术，更是梦想！！！'
    article_guoji = Article.objects.filter(sort2_ID='国际').order_by('-created_time')[:50]
    article_guonei = Article.objects.filter(sort2_ID='国内').order_by('-created_time')[:50]
    article_junshi = Article.objects.filter(sort2_ID='军事').order_by('-created_time')[:50]
    article_hangkong = Article.objects.filter(sort2_ID='航空').order_by('-created_time')[:50]
    return render(request, 'wangyi.html', locals())


# 网易新闻内联
def article_detail(request,sid):
    show = Article.objects.get(id=sid)
    return render(request, 'article_detail.html', locals())


# 诗词名句网
def Poetry(request):
    return render(request, 'Poetry.html', locals())


# 关于博主
def about(request):
    return render(request, 'about.html', locals())


# 给我留言
def message(request):
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    res = {'status': None, 'info': None}
    if request.method == 'POST':
        print(123456489)
        comment_name = request.POST.get('author')
        comment_content = request.POST.get('comment')
        print(comment_name, comment_content)
        if comment_name and comment_content:
            comment = guestbook.objects.create(comment_content=comment_content,
                                         create_time=now,
                                         comment_name=comment_name)
            if comment:
                res['status'] = 0
                res['info'] = '评论成功'
            else:
                res['status'] = 1
                res['info'] = '评论失败'
        if not comment_name or not comment_content:
            res['status'] = 2
            res['info'] = '昵称/内容未填写'
        return HttpResponse(json.dumps(res))
    comment = guestbook.objects.all().order_by('-AUTOADDCLMN')
    return render(request, 'message.html', locals())


# 我的博客园
def nmsghgnv(request):
    article = Article.objects.filter(source='我的博客园').order_by('-modified_time')
    currentPage = int(request.GET.get('page', 1))  # 获取当前在第几页
    paginator = Paginator(article, 5)  # 告诉分页器我5条分页
    # 如果总页数大于十一页，设置分页
    if paginator.num_pages > 11:
        # 如果当前页数小于5页
        if currentPage - 5 < 1:
            # 页面上显示的页码
            pageRange = range(1, 11)
        # 如果当前页数+5大于总页数显示的页码
        elif currentPage + 5 > paginator.num_pages:
            pageRange = range(paginator.num_pages - 9, paginator.num_pages + 1)
        else:
            # 在中间显示的十个页码
            pageRange = range(currentPage - 5, currentPage + 5)
    else:
        pageRange = paginator.page_range
    # 捕获路由异常
    try:
        article = paginator.page(currentPage)
    # 如果页码输入不是整数则返回第一页的数据
    except PageNotAnInteger:
        article = paginator.page(1)
    # 如果页码输入是空值则返回第一页数据
    except EmptyPage:
        article = paginator.page(1)
    return render(request, 'nmsghgnv.html', locals())


