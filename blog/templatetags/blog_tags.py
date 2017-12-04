from ..models import Post, Category, Tag
from django import template
from django.db.models.aggregates import Count


register = template.Library()

# 自定义函数，并注册为模板标签
@register.simple_tag
def get_recent_post(num=5):
    return Post.objects.all().order_by('-created_time')[:num]


@register.simple_tag
def archives():
    # dates方法返回列表，列表的每一项为每一篇文章的创建时间，精确到月份，降序排列
    return Post.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    # return Category.objects.all()
    # annotate方法与all类似，可以返回所有的category，还可以用于统计每个分类下文章的数量，赋值给num_posts，相当于Category类增加了num_posts属性
    # 进一步做了过滤，文章数目小于或等于0的分类不显示
    # Count方法的参数值不能传入Post
    return Category.objects.annotate(num_posts=Count("post")).filter(num_posts__gt=0)

@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)