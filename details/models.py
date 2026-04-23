from django.db import models
from userauth.models import *

# player season
class Season(models.Model):
    player = models.ForeignKey(User,on_delete=models.CASCADE, related_name='season_model', null=True, blank=True)
    season_year = models.CharField(max_length=20,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.player.username


# player season month
class Month(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='months')
    month_name = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.month_name


# 1️⃣ Player Model (Leaderboard)
class PlayerWeekdetails(models.Model):
    month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name='player_weekdetails')
    week_name = models.CharField(max_length=50, unique=True, null=True)
    goal = models.IntegerField(default=0)
    matches = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    goal_canceled = models.IntegerField(default=0)
    hattricks = models.IntegerField(default=0)
    clean_sheets = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.short_name


# 2️⃣ Match Model (Schedule / Results)
    
class PlayerMatch(models.Model):
    STATUS_CHOICES = [
        ("upcoming", "Upcoming"),
        ("live", "Live"),
        ("finished", "Finished"),
    ]
    team_name = models.CharField(max_length=100)
    date = models.DateTimeField()
    status = models.CharField(max_length=100,choices=STATUS_CHOICES)
    home_score = models.IntegerField(default=0, null=True)
    away_score = models.IntegerField(default=0, null=True)
    completion = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.team_name



# 3️⃣ Match Model (Schedule / Results)
class Match(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    match = models.ForeignKey(PlayerMatch, on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True)
    goals = models.IntegerField(default=0)
    goal_cancel = models.IntegerField(default=0)
    notes = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.team1} vs {self.team2}"
    



# 4 News Model
class News(models.Model):
    CHOICE_CATEGORY =  [
        ("General", "General"),
        ("Player", "Player"),
        ("League", "League"),
        ("Injury", "Injury"),
        ("Transfer", "Transfer")
    ]
    image = models.URLField(default="")
    headline = models.CharField(max_length=300)
    content = models.TextField()
    date = models.DateTimeField()
    category = models.CharField(max_length=100, choices=CHOICE_CATEGORY)
    hot = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


