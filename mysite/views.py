import datetime
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from django.urls import reverse
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
from article.models import Article


def get_7_days_hot_articles():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    articles = Article.objects \
                .filter(read_details__date__lt=today, read_details__date__gte=date) \
                .values('id', 'title') \
                .annotate(read_num_sum=Sum('read_details__read_num')) \
                .order_by('-read_num_sum')
    return articles[:7]

def home(request):
    article_content_type = ContentType.objects.get_for_model(Article)
    dates, read_nums = get_seven_days_read_data(article_content_type)

    # 获取7天热门文章的缓存数据
    hot_articles_for_7_days = cache.get('hot_articles_for_7_days')
    if hot_articles_for_7_days is None:
        hot_articles_for_7_days = get_7_days_hot_articles()
        cache.set('hot_articles_for_7_days', hot_articles_for_7_days, 3600)

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data(article_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(article_content_type)
    context['hot_articles_for_7_days'] = hot_articles_for_7_days
    return render(request, 'home.html', context)
