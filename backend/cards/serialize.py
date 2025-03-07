from rest_framework import serializers
from .models import Card

class CardSerializer(serializers.ModelSerializer):
    cvv = serializers.CharField(write_only=True, required=True)  

    class Meta:
        model = Card
        fields = [
            'id', 'user', 'card_holder_name', 'bin', 'last_four_digits', 
            'expiration_month', 'expiration_year', 'brand', 'active', 
            'selected', 'created_at', 'updated_at', 'cvv'
        ]
        extra_kwargs = {
            'bin': { 'write_only': True },  # Prevent BIN from being exposed in responses
            'cvv': {'write_only': True},  # Prevent CVV from being exposed in responses
        }

    def create(self, validated_data):
        """Encrypt CVV before saving."""
        cvv = validated_data.pop('cvv', None)  # Extract CVV from input data
        card = Card.objects.create(**validated_data)
        
        if cvv:
            card.set_cvv(cvv)  # Encrypt and store CVV
            card.save()
        
        return card

    def update(self, instance, validated_data):
        allowed_fields = {'active', 'selected'}  # Define fields that can be updated
        filtered_data = {key: value for key, value in validated_data.items() if key in allowed_fields}
        
        card = Card.objects.get(id=instance.id)
        card.selected = validated_data.get('selected')
        return super().update(instance, filtered_data)
    
    def patch(self, instance, validated_data):
        allowed_fields = {'active', 'selected'}  # Define fields that can be updated
        filtered_data = {key: value for key, value in validated_data.items() if key in allowed_fields}
        
        return super().update(instance, filtered_data)

        
