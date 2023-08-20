from django.shortcuts import render
from blog.models import Post, Comment
from blog.forms import CommentForm

# Create your views here.
def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {
        "posts": posts,
    }
    return render(request, "blog_index.html", context)


def blog_category(request, category):
    posts = Post.objects.filter(categories__name__contains=category).order_by(
        "-created_on"
    )
    context = {
        "category": category,
        "posts": posts,
    }

    return render(request, "blog_category.html", context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)

    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                content=form.cleaned_data["content"],
                post=post,
            )
            comment.save()
        else:
            print("Comment is invalid")

    comments = Comment.objects.filter(post=post)
    context = {"post": post, "comments": comments, "form": form}
    return render(request, "blog_detail.html", context)
