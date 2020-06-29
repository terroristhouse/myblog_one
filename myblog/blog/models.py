from django.db import models
from DjangoUeditor.models import UEditorField #头部增加这行代码导入UEditorField
from django.contrib.auth.models import User
# 导入Django自带用户模块

# 导航表
class Daohang(models.Model):
    name = models.CharField('导航条',max_length=100)

    class Meta:
        verbose_name = '导航条'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 文章分类
class Category(models.Model):
    name = models.CharField('博客分类', max_length=100)
    index = models.IntegerField(default=999, verbose_name='分类排序')

    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 文章标签
class Tag(models.Model):
    name = models.CharField('文章标签', max_length=100)

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 推荐位
class Tui(models.Model):
    name = models.CharField('推荐位', max_length=100)

    class Meta:
        verbose_name = '推荐位'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 文章
class Article(models.Model):
    title = models.CharField('标题', max_length=255)
    url = models.CharField('url',max_length=500)
    sort2_ID = models.CharField('类别',max_length=255,null=True,blank=True)
    excerpt = models.TextField('摘要', max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='分类', blank=True, null=True)
    # 使用外键关联分类表与分类是一对多关系
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    # 使用外键关联标签表与标签是多对多关系
    img = models.ImageField(upload_to='article_img/%Y/%m/%d/', verbose_name='文章图片', blank=True, null=True)
    body = UEditorField('内容', width=800, height=500,
                        toolbars="full", imagePath="upimg/", filePath="upfile/",
                        upload_settings={"imageMaxSize": 1204000},
                        settings={}, command=None, blank=True
                        )

    source = models.CharField(max_length=255,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者',null=True,blank=True)
    """
    文章作者，这里User是从django.contrib.auth.models导入的。
    这里我们通过 ForeignKey 把文章和 User 关联了起来。
    """
    views = models.PositiveIntegerField('阅读量', default=0)
    tui = models.ForeignKey(Tui, on_delete=models.DO_NOTHING, verbose_name='推荐位', blank=True, null=True)

    created_time = models.DateTimeField('发布时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)


    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'


    def __str__(self):
        return self.title


# Banner
class Banner(models.Model):
    text_info = models.CharField('标题', max_length=255, default='')
    img = models.ImageField('轮播图', upload_to='banner/')
    link_url = models.URLField('图片链接', max_length=255)
    is_active = models.BooleanField('是否是active', default=False)

    def __str__(self):
        return self.text_info

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = '轮播图'


# 友情链接
class Link(models.Model):
    name = models.CharField('链接名称', max_length=255)
    linkurl = models.URLField('网址', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = '友情链接'


# 名言表
class quote(models.Model):
    source = models.CharField(max_length=500, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    publishtime = models.DateTimeField(null=True, blank=True)
    ID = models.IntegerField(null=True, blank=True)
    AUTOADDCLMN = models.BigAutoField(primary_key=True)

    class Meta:
        verbose_name = '励志名言'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.source

# 名言评论表
class quote_comment(models.Model):
    comment_name = models.CharField(max_length=10)
    comment_content = models.CharField(max_length=500)
    create_time = models.DateTimeField()
    comment_image = models.CharField(max_length=255,null=True,blank=True)
    quotes = models.ForeignKey(quote,on_delete=models.CASCADE,verbose_name='名言')

    class Meta:
        verbose_name = '名言评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comment_name

# 留言板
class guestbook(models.Model):
    comment_content = models.CharField(max_length=500, null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True)
    comment_name = models.CharField(max_length=10, null=True, blank=True)
    comment_image = models.CharField(max_length=500, null=True, blank=True)
    AUTOADDCLMN = models.BigAutoField(primary_key=True)

    class Meta:
        verbose_name = '留言板'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comment_name



