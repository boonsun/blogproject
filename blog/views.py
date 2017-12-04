from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Category, Tag
import markdown
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q


# def index(request):
#     # return HttpResponse('Hello World')
#     # return render(request, 'blog/index.html', context={'title': '首页',
#     #                                                    'welcome': 'Hello World'})
#
#     # 按创建时间逆序排列，即最新的文章在最前面
#     # post_list = Post.objects.all().order_by('-created_time')
#     post_list = Post.objects.all()
#     return render(request, 'blog/index.html', context={'post_list': post_list})


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    # 启用分页
    paginate_by = 4


# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     # 支持markdown
#     # codehilite用于语法高亮
#     # toc用于自动生成目录
#     post.body = markdown.markdown(post.body,
#                                   extensions=['markdown.extensions.extra',
#                                               'markdown.extensions.codehilite',
#                                               'markdown.extensions.toc'])
#
#     form = CommentForm()
#     comment_list = post.comment_set.all()
#     context = {
#         'post': post,
#         'form': form,
#         'comment_list': comment_list,
#     }
#
#     # 调用一次detail方法，阅读量加1
#     post.increase_views()
#
#     # return render(request, 'blog/detail.html', context={'post': post})
#     return render(request, 'blog/detail.html', context=context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    # 将阅读量加1
    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)

        # post.body = markdown.markdown(post.body,
        #                               extensions=['markdown.extensions.extra',
        #                                           'markdown.extensions.codehilite',
        #                                           'markdown.extensions.toc'])

        # md = markdown.Markdown(extensions=['markdown.extensions.extra',
        #                                    'markdown.extensions.codehilite',
        #                                    'markdown.extensions.toc'])

        md = markdown.Markdown(
            extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite', TocExtension(slugify=slugify)])

        # 将markdown文本转换为HTML文本，转换后md会多出toc属性
        post.body = md.convert(post.body)
        # 目录
        post.toc = md.toc

        return post

    # 复写get_context_data方法，是为了将表单和评论传递给模板
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })

        return context


# def archives(request, year, month):
#     # filter方法用于过滤文章
#     # post_list = Post.objects.filter(created_time__year=year, created_time__month=month).order_by('-created_time')
#     post_list = Post.objects.filter(created_time__year=year, created_time__month=month)
#     return render(request, 'blog/index.html', context={'post_list': post_list})


class ArchivesView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year, created_time__month=month)


# class CategoryView(ListView):
#     model = Post
#     template_name = 'blog/index.html'
#     context_object_name = 'post_list'
#
#
#     # 复写父类的get_queryset方法。该方法默认获取全部列表数据
#     def get_queryset(self):
#         # kwargs 属性返回字典，从中提取pk的值
#         cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
#         return super(CategoryView, self).get_queryset().filter(category=cate)

# CategoryView的属性值和IndexView一样，甚至可以继承IndexView
class CategoryView(IndexView):
    # 复写父类的get_queryset方法。该方法默认获取全部列表数据
    def get_queryset(self):
        # kwargs 属性返回字典，从中提取pk的值
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     # post_list = Post.objects.filter(category=cate).order_by('-created_time')
#     post_list = Post.objects.filter(category=cate)
#     return render(request, 'blog/index.html', context={'post_list': post_list})

class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "请输入关键词"
        return render(request, 'blog/index.html', {"error_msg": error_msg})

    # icontains中的i表示不区分大小写
    # post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    post_list = Post.objects.filter(title__icontains=q)
    return render(request, 'blog/index.html', {"error_msg": error_msg,
                                               'post_list': post_list})
