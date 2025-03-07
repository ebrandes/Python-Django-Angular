from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom serializer to include user ID in JWT token"""
    
    def validate(self, attrs):
        """Customize token response to include user ID"""
        data = super().validate(attrs)
        data["user_id"] = self.user.id  # Include user ID in token payload
        return data
