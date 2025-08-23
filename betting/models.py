import uuid
from django.db import models

class Event(models.Model):
    """
    投票対象となるイベント
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Option(models.Model):
    """
    イベントの選択肢
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="options"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.event.title} - {self.name}"


class Bet(models.Model):
    """
    どの選択肢にいくら投票したか
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    option = models.ForeignKey(
        Option,
        on_delete=models.CASCADE,
        related_name="bets"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    username = models.CharField(max_length=50, default="anonymous")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bet {self.amount} on {self.option.name}"
