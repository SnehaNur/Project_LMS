from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        read_only_fields = fields  # All fields are read-only for admin viewing


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username']
        
    def update(self, instance, validated_data):
        # Prevent updating of username if needed
        if 'username' in validated_data:
            validated_data.pop('username')
        return super().update(instance, validated_data)
    

class UserdetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Show all fields in the user model
        fields = ['first_name','last_name','username','email','contact_number','date_joined']
        read_only_fields = ['first_name','last_name','username','email','contact_number','date_joined']

    def update(self, instance, validated_data):
        # Prevent updating sensitive fields
        for field in ['username', 'password']:
            validated_data.pop(field, None)
        return super().update(instance, validated_data)
