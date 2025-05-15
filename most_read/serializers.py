from rest_framework import serializers
from bookAPI.models import RecentRead

class ReaderBookSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = RecentRead
        fields = ['username', 'book_id']
