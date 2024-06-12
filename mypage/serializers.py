from rest_framework import serializers
from .models import MovieHistory

class MovieHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieHistory
        fields = '__all__'

    def create(self, validated_data):
        return MovieHistory.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.user = validated_data.get('user')
        instance.title = validated_data.get('title')
        instance.content = validated_data.get('content')
        instance.poster = validated_data.get('poster')
        instance.year = validated_data.get('year')
        instance.month = validated_data.get('month')
        instance.day = validated_data.get('day')
        instance.save()
        return instance
    
    def delete(self, id):
        return MovieHistory.objects.filter(id=id).delete()

    def get_by_user(user):
        return MovieHistory.objects.filter(user=user)
    
    def get_by_id(self,id):
        return MovieHistory.objects.filter(id = id)