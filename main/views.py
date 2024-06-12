from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework import serializers
from .models import *
from .serializers import *
from django.shortcuts import render, get_object_or_404
from .models import Cinema
from rest_framework.renderers import TemplateHTMLRenderer

# Create your views here.
class Cinema_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = '__all__'

class Star_Cinema_List(APIView): # stagr - desc
    def get(self, request):
        cinemas = Cinema.objects.all().order_by('-star')
        serializer = Cinema_Serializer(cinemas, many = True)
        return Response(serializer.data)
    
class Name_Cinema_List(APIView): # abcd... - asc
    def get(self, request):
        cinemas = Cinema.objects.all().order_by('name')
        serializer = Cinema_Serializer(cinemas, many = True)
        return Response(serializer.data)
    
class Like_Cinema_List(APIView): # like - asc
    def get(self, request):
        cinemas = Cinema.objects.all().order_by('-like_cnt')
        serializer = Cinema_Serializer(cinemas, many = True)
        return Response(serializer.data)

class Cinema_List(generics.ListAPIView):        # 영화관 리스트 가져오기
    queryset = Cinema.objects.all()
    serializer_class = Cinema_Serializer

class Detail_Info_Cinema(generics.RetrieveAPIView): # cinema detail info
    queryset = Cinema.objects.all()
    serializer_class = Cinema_Detail

class Like_Cinema(APIView): # like 증가. runserver 하고 우하단 POST 버튼 누르면 like 1씩 증가.
    def post(self, request, pk):
        try:
            cinema = Cinema.objects.get(pk=pk)
            cinema.like_cnt += 1
            cinema.save()
            return Response({'status' : 'success', 'like' : cinema.like_cnt}, status=status.HTTP_200_OK)
        except Cinema.DoesNotExist:
            return RecursionError({'error': 'Cinema not found'}, status=status.HTTP_404_NOT_FOUND)
        
class Location_Cinema_List(APIView):
    def get(self, request, location_name):
        cinemas = Cinema.objects.filter(location = location_name)
        serializers = Cinema_Serializer(cinemas, many = True)
        return Response(serializers.data)
    
class Seoul_Cinema_List(APIView): # location 변경하여 다른 지역구 영화관 검색 가능
    def get(self, request):
        cinemas = Cinema.objects.filter(location = "서울")
        serializers = Cinema_Serializer(cinemas, many = True)
        return Response(serializers.data)

def cinema_location_map(request, pk): # use X
    cinema = get_object_or_404(Cinema, pk=pk)
    return render(request, 'main/map.html', {'cinema': cinema})

class Rate_Cinema(APIView):
    def post(self, request, pk):
        try:
            cinema = Cinema.objects.get(pk=pk)
        except Cinema.DoesNotExist:
            return Response({'error': 'Cinema not found'}, status=status.HTTP_404_NOT_FOUND)
        
        rating = request.data.get('rating')
        if rating is not None:
            try:
                rating = Decimal(rating)
                if 0.0 <= rating <= 5.0:
                    cinema.update_rating(rating)
                    return Response({'status': 'success', 'rating': cinema.star}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Rating must be between 0 and 5'}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({'error': 'Invalid rating value'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Rating is required'}, status=status.HTTP_400_BAD_REQUEST)