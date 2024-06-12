from django.urls import path, include
from rest_framework import routers
from . import views
from .views import CommunityViewSet, CommunityDetailViewSet,CommunityCommentViewSet, CommentViewSet, CommunityPostViewSet, CommunityListViewSet

app_name = "community"

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("all", CommunityListViewSet, basename="community")

community_detail_router = routers.SimpleRouter(trailing_slash=False)
community_detail_router.register("communities", CommunityDetailViewSet, basename="commuinties-detail")

community_post_router = routers.SimpleRouter(trailing_slash=False)
community_post_router.register("communities/posts", CommunityPostViewSet, basename="commuinties-post")

community_comment_router = routers.SimpleRouter(trailing_slash=False)
community_comment_router.register("comments", CommunityCommentViewSet, basename="comments") #리스트조회, 작성

comment_router = routers.SimpleRouter(trailing_slash=False)
comment_router.register("comments", CommentViewSet, basename="comments") #수정, 삭제

community_detail_action = {
    'get' : 'retrieve',
    'post' : 'like_action',
    'delete' : 'like_action'
}

urlpatterns = [
    # 게시물 전체
    path('communities/', include(default_router.urls)),

    # 게시글 작성, 수정, 삭제
    path('', include(community_post_router.urls)),

    #게시글 리스트
    path('communities/tips', views.CommunityViewSet.as_view({'get': 'list'}), {'category': 'cinema_tip'}, name='community-cinema_tip'),
    path('communities/commons', views.CommunityViewSet.as_view({'get': 'list'}), {'category': 'common'}, name='community-common'),
    path('communities/suggestions', views.CommunityViewSet.as_view({'get': 'list'}), {'category': 'suggestion'}, name='community-suggestion'),

    # 디테일페이지 url
    path('communities/tips/<int:pk>', views.CommunityDetailViewSet.as_view(community_detail_action), {'category': 'cinema_tip'}, name='community-cinema_tip-detail'),
    path('communities/commons/<int:pk>', views.CommunityDetailViewSet.as_view(community_detail_action), {'category': 'common'}, name='community-common-detail'),
    path('communities/suggestions/<int:pk>', views.CommunityDetailViewSet.as_view(community_detail_action), {'category': 'suggestion'}, name='community-suggestion-detail'),

    path('communities/posts/<int:community_id>/', include(community_comment_router.urls)),
    path('communities/posts/', include(comment_router.urls)),

    # 관리자가 접수 여부를 수정하는 URL
    path('communities/<int:pk>/update-received', views.CommunityViewSet.as_view({'patch': 'update_received'}), name='community-update-received'),
]
