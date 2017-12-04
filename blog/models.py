from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags
import markdown


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    # verbose_name可以设置别名
    title = models.CharField(max_length=100, verbose_name='标题')
    body = models.TextField()

    created_time = models.DateField()
    modified_time = models.DateField()

    # 摘要，允许为空
    excerpt = models.CharField(max_length=200, blank=True)

    # 分类，一篇文章只能有一个分类，但一个分类下可以有多篇文章
    # ForeignKey表示一对多
    category = models.ForeignKey(Category)

    # 标签，多对多，且允许为空
    tags = models.ManyToManyField(Tag, blank=True)

    # User是django内置的用户模型（类），一对多
    author = models.ForeignKey(User)

    # 文章阅读量
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_time', 'title']

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    # 复写save方法，提取body的前面一些字符，赋值给excerpt，并保存到数据库
    # 有一个问题，摘要不会实时更新
    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite'
            ])

            # strip_tags用于去掉HTML文本的HTML标签
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的save方法将数据保存到数据库
        super(Post, self).save(*args, **kwargs)
