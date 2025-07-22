from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm
from django.contrib import messages
from .models import Article, Comment
from .forms import CommentForm

@login_required
def list_articles(request):
    articles = Article.objects.filter(author=request.user)
    return render(request, 'articles/list_articles.html', {'articles': articles})


@login_required
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, "Article added successfully!")
            return redirect('list_articles')
    else:
        form = ArticleForm()
    return render(request, 'articles/add_article.html', {'form': form})


@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id, author=request.user)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Article updated successfully!")
            return redirect('list_articles')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/edit_article.html', {'form': form, 'article': article})


@login_required
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id, author=request.user)
    article.delete()
    messages.success(request, "Article deleted successfully!")
    return redirect('list_articles')


def article_list(request):
    articles = Article.objects.all()
    return render(request, 'articles/article_list.html', {'articles': articles})


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    comments = Comment.objects.filter(article=article)
    return render(request, 'articles/article_detail.html', {
        'article': article,
        'comments': comments,
    })


# articles/views.py




@login_required
def like_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
    return redirect('article_detail', article_id=article_id)

@login_required
def add_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
    return redirect('article_detail', article_id=article_id)
