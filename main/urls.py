from django.urls import path, include
from .views import *

urlpatterns = [
    path('cinemas/', Cinema_List.as_view(), name='cinema_list'),
    path('cinemas_star/', Star_Cinema_List.as_view(), name = 'star_cinema'),
    path('cinemas_name/', Name_Cinema_List.as_view(), name = 'name_cinema'),
    path('cinemas_like/', Like_Cinema_List.as_view(), name = 'like_cinema'),
    path('cinemas/detail/<int:pk>/', Detail_Info_Cinema.as_view(), name = 'detail_cinema'),
    path('cinemas/like/<int:pk>/', Like_Cinema.as_view(), name = 'like_plus'),
    # path('cinemas/location/<str:location_name>/', Location_Cinema_List.as_view(), name = 'location_cinema'), # <str:location_name>에 해당 지역명 넣으면 됨
    #path('cinemas/seoul/', Seoul_Cinema_List.as_view(), name = 'seoul_cinema'), # 미사용
    path('cinemas/map/<int:pk>/', cinema_location_map, name='cinema_map'),
    path('cinemas/rating/<int:pk>/', Rate_Cinema.as_view(), name = 'rating_cinema'),
]