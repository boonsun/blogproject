from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from .models import Comment
from .forms import CommentForm


def post_comment(request, post_pk):

    """
    第一次点击文章详情页，访问方式为get，则打开详情页
    下面提交评论时，若正确提交，将评论保存到数据库，然后重新打开详情页；
    若错误提交，最简单情况就是重新打开详情页，但最好渲染表单的错误
    
    """
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':

        # 用户提交的数据保存在request.POST中，用这些数据构造CommentForm实例
        form = CommentForm(request.POST)

        if form.is_valid():
            # commit = False的作用是仅仅利用表单的数据生成Comment模型类的实例，但还不保存评论数据到数据库
            comment = form.save(commit=False)
            # 将评论和文章关联起来
            comment.post = post
            # 最终将评论保存到数据库
            comment.save()

            # 重定向到文章的详情页
            # 实际上调用post的get_absolute_url方法，重定向到该方法返回的url
            return redirect(post)

        else:
            # 获取文章下的所有评论
            # 等价于Comment.objects.filter(post=post)
            comment_list = post.comment_set.all()
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list
            }

            return render(request, 'blog/detail.html', context=context)

    # 不是POST请求时，返回文章详情页
    return redirect(post)
