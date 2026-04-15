from django.db import models
from userauth.models import *



# player season
class Season(models.Model):
    player = models.ForeignKey(User,on_delete=models.CASCADE, related_name='season_model', null=True, blank=True)
    season_year = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# player season month
class Month(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='months')
    month_name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# 1️⃣ Player Model (Leaderboard)
class PlayerWeekdetails(models.Model):
    month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name='player_weekdetails')
    # short_name = models.CharField(max_length=50)

    # points = models.IntegerField(default=0)
    goal = models.IntegerField(default=0)
    matches = models.IntegerField(default=0)

    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)

    # goal = models.IntegerField(default=0)
    goal_canceled = models.IntegerField(default=0)

    # rank = models.IntegerField(default=0)
    hattricks = models.IntegerField(default=0)
    clean_sheets = models.IntegerField(default=0)

    # form_average = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.short_name


# 2️⃣ Match Model (Schedule / Results)
class Match(models.Model):
    STATUS_CHOICES = [
        ("upcoming", "Upcoming"),
        ("live", "Live"),
        ("finished", "Finished"),
    ]

    team1 = models.CharField(max_length=200, null=True)
    team2 = models.CharField(max_length=200, null=True)

    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)

    time = models.TimeField(null=True)
    date = models.DateField(null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True)

    score = models.CharField(max_length=20, blank=True, null=True)
    result_type = models.CharField(max_length=50, blank=True, null=True)
    result_label = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.team1} vs {self.team2}"


# 3️⃣ News Model
class News(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    content = models.TextField()

    time = models.DateTimeField()
    category = models.CharField(max_length=100)

    hot = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


