from rest_framework.response import Response
from rest_framework import viewsets, status, mixins, generics
from rest_framework.decorators import api_view
from accounts.models import User, UserManager
#from accounts.serializers import serializer
from accounts.serializers import UserSerializer
from django.shortcuts import render
from rest_framework.response import Response
import requests
import json
from rest_framework.views import APIView
from .models import MovieHistory
from .serializers import MovieHistorySerializer
from django.shortcuts import get_object_or_404
from community.models import *
from community.serializers import *

from django.contrib.auth import get_user_model
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.permissions import IsAuthenticated


class MyProfileViewSet(generics.RetrieveUpdateAPIView): # 조회랑 수정만 할 거니까
    serializer_class = UserSerializer
    http_method_names = ['get','put', 'patch']
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)
    
# @api_view(['GET'])
# def get_user_profile(request):
    # user = request.user    
    # user_serializer = UserSerializer(user).data
#     return Response({"user" : user_serializer}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_movie_history(request):
    user = request.user    
    movie_histories = MovieHistorySerializer.get_by_user(user=user)
    movie_histories_serializer = MovieHistorySerializer(movie_histories, many=True)
    return Response({"movie_history" : movie_histories_serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_community_history(request):
    user = request.user        
    communities = Community.objects.filter(writer=user)
    communities_serializer = CommunitySerializer(communities, many=True)
    return Response({"communities" : communities_serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_community_history(request):
    user = request.user        
    comments = CommunityComment.objects.filter(writer=user)
    comments_serializer = CommunityCommentSerializer(comments, many=True)
    return Response({"comments" : comments_serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_like_posts(request):
    user = request.user    
    likePosts = CommunityLike.objects.filter(user=user)
    likePosts_ids = likePosts.values_list('community', flat=True)
    liked_communities = Community.objects.filter(id__in=likePosts_ids)
    likePosts_serializer = LikePostsSerializer(likePosts, many=True)
    liked_communities_serializer = CommunitySerializer(liked_communities, many=True)

    return Response({"likes" : liked_communities_serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_profile(request):
    user = request.user    
    user_serializer = UserSerializer(user).data
    movie_histories = MovieHistorySerializer.get_by_user(user=user)
    movie_histories_serializer = MovieHistorySerializer(movie_histories, many=True)
    
    communities = Community.objects.filter(writer=user)
    communities_serializer = CommunitySerializer(communities, many=True)

    comments = CommunityComment.objects.filter(writer=user)
    comments_serializer = CommunityCommentSerializer(comments, many=True)

    likePosts = CommunityLike.objects.filter(user=user)
    likePosts_serializer =  LikePostsSerializer(likePosts, many=True)

    res = Response(
            {
                "message" : "Getting Profile success",
                "user" : user_serializer,
                "communities" : communities_serializer.data,
                "comments" : comments_serializer.data,
                "likePost" : likePosts_serializer.data,
                "movieHistory" : movie_histories_serializer.data,
            },
            status = status.HTTP_200_OK,
        )
    
    return res


# @api_view(['POST'])
# def modify_profile(request):
#     user=request.user
#     email = user.email
#     nickname = request.data.get('nickname')
#     user.update_user(email=email, nickname=nickname)
#     user_serializer = UserSerializer(user).data

#     res = Response(
#             {
#                 "message" : "Getting Profile success",
#                 "user" : user_serializer,
#             },
#             status = status.HTTP_200_OK,
#         )
    
#     return res


@api_view(['POST'])
def create_movieHistory(request):
    user = request.user
    data = {
        'user' : user,
        'title': request.data.get('title'),
        'content': request.data.get('content'),
        'poster': request.data.get('poster'),
        'year': request.data.get('year'),
        'month': request.data.get('month'),
        'day': request.data.get('day'),
    } 
    serializer = MovieHistorySerializer()
    movie_history = serializer.create(data)  # Pass user instance directly here
    return Response(MovieHistorySerializer(movie_history).data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_movieHistory(request):
    user = request.user
    movie_histories = MovieHistorySerializer.get_by_user(user=user)
    serializer = MovieHistorySerializer(movie_histories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def update_movieHistory(request):
    user = request.user
    data = {
        'user': user,
        'title': request.data.get('title'),
        'content': request.data.get('content'),
        'poster' : request.data.get('poster'),
        'year': request.data.get('year'),
        'month': request.data.get('month'),
        'day': request.data.get('day'),
    }
    id = request.data.get('id')
    movie_history = get_object_or_404(MovieHistory, id=id)
    
    serializer = MovieHistorySerializer()
    
    modified_instance = serializer.update(movie_history, data)
    return Response(MovieHistorySerializer(modified_instance).data)
    
@api_view(['POST'])
def remove_movieHistory(request):
    id = request.data.get('id')
    serializer = MovieHistorySerializer()
    serializer.delete(id)
    return Response({'message':'delete success'}, status=status.HTTP_200_OK)
