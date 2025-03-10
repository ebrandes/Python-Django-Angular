from rest_framework import serializers

from cards.models import Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [
            "id",
            "user",
            "last_four_digits",
            "holder",
            "expiry_year",
            "expiry_month",
            "branch",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
