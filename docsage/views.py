# views.py
from django.shortcuts import render
from django.db.models import Count  # Import Count for aggregation
from articles.models import Article
from users.models import Review

def home(request):
    # Fetch all articles and annotate with total likes
    articles_by_likes = Article.objects.filter(status='published').annotate(
        total_likes_count=Count('likes')  # Correct use of Count
    ).order_by('-total_likes_count', '-created_at')  # Sort by total likes and creation date

    # Fetch the latest 3 reviews
    latest_reviews = Review.objects.order_by('-created_at')[:10]

    return render(request, 'home.html', {
        'articles_by_likes': articles_by_likes,
        'latest_reviews': latest_reviews,
    })


def about(request):
    return render(request, 'about.html')
