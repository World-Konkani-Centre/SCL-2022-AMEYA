from rest_framework import serializers
from .models import Business,RegisteredBusiness
#searializer for business model:
class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model=Business
        fields='__all__'

#searializer for registered business model:
class RegisteredBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model=RegisteredBusiness
        fields='__all__'