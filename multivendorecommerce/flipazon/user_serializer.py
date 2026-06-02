from rest_framework import serializers
from .models import Usermodel
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usermodel
        fields = '__all__'

    def validate(self,value):
        data=Usermodel.objects.filter(email=value)
        if data.exists():
            raise serializers.ValidationError("Email already exists")
        return value