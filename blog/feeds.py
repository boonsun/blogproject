from .models import Post
from django.contrib.syndication.views import Feed


class AllPostRssFeed(Feed):
    title = 'Django 博客教程'

    link = '/'

    description = 'Django 测试文章'

    def item(self):
        return Post.objects.all()

    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    def item_description(self, item):
        return item.body
