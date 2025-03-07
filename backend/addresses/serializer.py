from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
