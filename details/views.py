from .models import Player, Match, News

from .serializers import PlayerRankingSerializer, MatchSerializer, NewsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PlayerRankingView(APIView):
    def get(self, request):
        players = Player.objects.all().order_by('-points', '-goals', 'matches')
        serializer = PlayerRankingSerializer(players, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class MatchListView(APIView):
    def get(self, request):
        matches = Match.objects.all().order_by('-date', '-time')
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class NewsListView(APIView):
    def get(self, request):
        news = News.objects.all().order_by('-created_at')
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)