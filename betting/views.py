# betting/views.py
from decimal import Decimal
from django.db.models import Sum
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event, Option, Bet
from .serializers import EventSerializer, OptionSerializer, BetSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    イベントの作成・取得・更新・削除
    選択肢の追加と出馬表(board)表示を含む
    """
    queryset = Event.objects.all().order_by("-created_at")
    serializer_class = EventSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["id", "title"]

    @action(detail=True, methods=["post"])
    def add_option(self, request, pk=None):
        """
        イベントに選択肢を追加する
        POST body: { "name": "Option name" }
        """
        event = self.get_object()
        name = request.data.get("name")
        if not name:
            return Response({"error": "name is required"}, status=400)
        opt = Option.objects.create(event=event, name=name)
        return Response(OptionSerializer(opt).data)

    @action(detail=True, methods=["get"])
    def board(self, request, pk=None):
        """
        出馬表 (総プール、各選択肢の賭け金合計とオッズ) を返す
        """
        event = self.get_object()
        # 総プール
        total_pool = Bet.objects.filter(option__event=event).aggregate(
            s=Sum("amount")
        ).get("s") or Decimal("0")

        options_data = []
        for opt in event.options.all():
            total_amount = (
                Bet.objects.filter(option=opt).aggregate(s=Sum("amount")).get("s")
                or Decimal("0")
            )
            odds = float(total_pool / total_amount) if total_amount > 0 else None
            options_data.append(
                {
                    "option_id": opt.id,
                    "name": opt.name,
                    "total_amount": str(total_amount),
                    "odds": odds,
                }
            )

        data = {
            "event_id": event.id,
            "title": event.title,
            "total_pool": str(total_pool),
            "options": options_data,
        }
        return Response(data)


class OptionViewSet(viewsets.ModelViewSet):
    """
    選択肢のCRUD
    """
    queryset = Option.objects.all().order_by("id")
    serializer_class = OptionSerializer
    
    @action(detail=True, methods=["get"])
    def bets(self, request, pk=None):
        """
        /api/options/{id}/bets/ で該当OptionのBet一覧（最新順）を返す
        """
        option = self.get_object()
        qs = option.bets.all().order_by("-created_at")
        return Response(BetSerializer(qs, many=True).data)


class BetViewSet(viewsets.ModelViewSet):
    """
    投票 (Bet) のCRUD
    """
    queryset = Bet.objects.all().order_by("-created_at")
    serializer_class = BetSerializer
