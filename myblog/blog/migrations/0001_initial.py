# Generated by Django 2.1.8 on 2020-05-11 14:48

import DjangoUeditor.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, verbose_name='标题')),
                ('excerpt', models.TextField(blank=True, max_length=200, verbose_name='摘要')),
                ('img', models.ImageField(blank=True, null=True, upload_to='article_img/%Y/%m/%d/', verbose_name='文章图片')),
                ('body', DjangoUeditor.models.UEditorField(blank=True, verbose_name='内容')),
                ('source', models.CharField(blank=True, max_length=255, null=True)),
                ('views', models.PositiveIntegerField(default=0, verbose_name='阅读量')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
            },
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_info', models.CharField(default='', max_length=50, verbose_name='标题')),
                ('img', models.ImageField(upload_to='banner/', verbose_name='轮播图')),
                ('link_url', models.URLField(max_length=100, verbose_name='图片链接')),
                ('is_active', models.BooleanField(default=False, verbose_name='是否是active')),
            ],
            options={
                'verbose_name': '轮播图',
                'verbose_name_plural': '轮播图',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='博客分类')),
                ('index', models.IntegerField(default=999, verbose_name='分类排序')),
            ],
            options={
                'verbose_name': '博客分类',
                'verbose_name_plural': '博客分类',
            },
        ),
        migrations.CreateModel(
            name='guestbook',
            fields=[
                ('comment_content', models.CharField(blank=True, max_length=500, null=True)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
                ('comment_name', models.CharField(blank=True, max_length=5, null=True)),
                ('comment_image', models.CharField(blank=True, max_length=500, null=True)),
                ('AUTOADDCLMN', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': '留言板',
                'verbose_name_plural': '留言板',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='链接名称')),
                ('linkurl', models.URLField(max_length=100, verbose_name='网址')),
            ],
            options={
                'verbose_name': '友情链接',
                'verbose_name_plural': '友情链接',
            },
        ),
        migrations.CreateModel(
            name='quote',
            fields=[
                ('source', models.CharField(blank=True, max_length=500, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('publishtime', models.DateTimeField(blank=True, null=True)),
                ('ID', models.IntegerField(blank=True, null=True)),
                ('AUTOADDCLMN', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': '励志名言',
                'verbose_name_plural': '励志名言',
            },
        ),
        migrations.CreateModel(
            name='quote_comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_name', models.CharField(max_length=10)),
                ('comment_content', models.CharField(max_length=500)),
                ('create_time', models.DateTimeField()),
                ('comment_image', models.CharField(blank=True, max_length=255, null=True)),
                ('quotes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.quote', verbose_name='名言')),
            ],
            options={
                'verbose_name': '名言评论',
                'verbose_name_plural': '名言评论',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='文章标签')),
            ],
            options={
                'verbose_name': '文章标签',
                'verbose_name_plural': '文章标签',
            },
        ),
        migrations.CreateModel(
            name='Tui',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='推荐位')),
            ],
            options={
                'verbose_name': '推荐位',
                'verbose_name_plural': '推荐位',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Category', verbose_name='分类'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, to='blog.Tag', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='article',
            name='tui',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Tui', verbose_name='推荐位'),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者'),
        ),
    ]