from django.urls import path
from .views import PlayerRankingView, MatchListView, NewsListView



urlpatterns = [
    path('player-rankings/', PlayerRankingView.as_view(), name='player-rankings'),
    path('matches/', MatchListView.as_view(), name='match-list'),
    path('news/', NewsListView.as_view(), name='news-list'),
]