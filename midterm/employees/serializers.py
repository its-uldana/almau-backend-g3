from rest_framework import serializers
from .models import Employees


class EmployeesSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255, allow_null=False)
    position = serializers.CharField(max_length=255, allow_null=False)
    salary = serializers.IntegerField(default=0, allow_null=False)
    
    def create(self, validated_data):
        employees = Employees(**validated_data)
        employees.save()
        return employees

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.save()
        return instance
