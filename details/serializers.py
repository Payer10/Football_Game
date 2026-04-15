from .models import PlayerWeekdetails, Match, News
from rest_framework import serializers


class PlayerRankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerWeekdetails
        fields = ['id', 'matches', 'wins', 'losses', 'draws', 'goal', 'goal_canceled', 'hattricks', 'clean_sheets']   
        # read_only_fields = ['id', 'short_name', 'points', 'goals', 'matches', 'wins', 'losses', 'draws', 'goals_for', 'goals_against', 'rank', 'hattricks', 'clean_sheets', 'form_average']


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'team1', 'team2', 'team1_score', 'team2_score', 'time', 'date', 'status', 'score', 'result_type', 'result_label']
        # read_only_fields = ['id', 'team1', 'team2', 'team1_score', 'team2_score', 'time', 'date', 'status', 'score', 'result_type', 'result_label']



class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'created_at']
        # read_only_fields = ['id', 'title', 'content', 'created_at']