from rest_framework import serializers
from .models import *

class Cinema_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = ['id', 'name', 'star', 'like_cnt', 'location']

class Movie_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'poster_url']

class Cinema_Detail(serializers.ModelSerializer):
    movies = Movie_Serializer(many=True, read_only=True)

    class Meta:
        model = Cinema
        fields = ['name', 'cite_url', 'star', 'like_cnt', 'view_url', 'discription', 'location', 'movies', 'tel', 'detail_loc']

    def get_movie(self, obj):
        movies = obj.moviews.all()
        return Movie_Serializer(movies, many = True).data

