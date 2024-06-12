from rest_framework import viewsets, mixins, filters, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from django.utils import timezone

from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.contrib.auth import get_user_model

from .models import Community, CommunityComment, CommunityLike
from .serializers import *
from .paginations import CommunityPagination
from .permissions import IsOwnerOrReadOnly

#리스트 생성
# class CommunityListCreate(generics.ListCreateAPIView):
#     queryset = Community.objects.all()
#     serializer_class = CommunityCreateUpdateSerializer

# 정렬 기능
class CommunityOrderingFilter(filters.OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        order_by = request.query_params.get(self.ordering_param)
        if order_by == 'popular':
            return queryset.order_by('-view_cnt') # 조회순
        elif order_by == 'like':
            return queryset.order_by('-likes_cnt') # 좋아요순
        else:
            # 기본은 최신순으로 설정
            return queryset.order_by('-created_at')
        
# 커뮤니티 목록
class CommunityViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Community.objects.all()
    filter_backends = [CommunityOrderingFilter, SearchFilter]
    search_fields = ['title', 'content', 'writer','cinema__name'] 
    pagination_class = CommunityPagination

    def get_serializer_class(self):
            queryset = self.get_queryset()
            category = queryset.values_list('category', flat=True).first()
            if category == 'cinema_tip':
                return TipListSerializer
            if category == 'common':
                return CommonListSerializer
            else:
                return SuggestionListSerializer
            
    def retrieve(self):
        instance = self.get_object()
        instance.view_cnt += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == "list":
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(writer = self.request.user)

    def get_queryset(self):
        category = self.kwargs.get('category')

        User = get_user_model()
        user = self.request.user if isinstance(self.request.user, User) else None

        queryset = Community.objects.filter(category=category).annotate(
            likes_cnt=Count('likes_community', distinct=True)
        )
        return queryset
    
    @action(methods=['patch'], detail=True, url_path='update-received', permission_classes=[IsAdminUser])
    def update_received(self, request, *args, **kwargs):
        instance = self.get_object()
        is_received = request.data.get('is_received')

        if is_received is not None:
            instance.is_received = is_received
            instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
        
# 게시물 작성 & 수정
class CommunityPostViewSet(viewsets.GenericViewSet,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin
                            ):
    serializer_class = CommunityCreateUpdateSerializer
    queryset = Community.objects.all()

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated()]
        else:
            return [IsOwnerOrReadOnly()]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        
        if 'title' in data or 'content' in data:
            instance.title = data.get('title', instance.title)
            instance.content = data.get('content', instance.content)
            instance.updated_at = timezone.now()
            instance.save()
            
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_cnt += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    # def perform_destroy(self, instance):
    #     serializer = self.get_serializer(instance)
    #     serializer.delete(instance)
        
# 커뮤니티 디테일
class CommunityDetailViewSet(viewsets.GenericViewSet,
                            mixins.RetrieveModelMixin,
                            ):
    def get_serializer_class(self):
            queryset = self.get_queryset()
            category = queryset.values_list('category', flat=True).first()
            if category == 'common':
                return CommonDetailSerializer
            if category == 'cinema_tip':
                return Cinema_tipDetailSerializer
            else:
                return SuggestionDetailSerializer
    
    def get_permissions(self):
        if self.action in ['like_action']:
            return [IsAuthenticated()]
        elif self.action in ['retrieve']:
            return [AllowAny()]
        else:
            return []
    
    def get_queryset(self):
        category = self.kwargs.get('category')

        User = get_user_model()
        user = self.request.user if isinstance(self.request.user, User) else None

        queryset = Community.objects.filter(category=category).annotate(
            likes_cnt=Count('likes_community', distinct=True)
        )
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_cnt += 1 
        instance.save()  

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=['POST', 'DELETE'], detail=True, url_path='like')
    def like_action(self, request, *args, **kwargs):
        community = self.get_object()
        user = request.user
        community_like, created = CommunityLike.objects.get_or_create(community=community, user=user)

        if request.method == 'POST':
            community_like.save()
            return Response({"detail": "좋아요를 눌렀습니다."})
        
        elif request.method == 'DELETE':
            community_like.delete()
            return Response({"detail": "좋아요를 취소하였습니다."})
        
# 커뮤니티 댓글 목록, 작성
class CommunityCommentViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    serializer_class = CommunityCommentSerializer
    # pagination_class = CommunityCommentPagination
    filter_backends = [CommunityOrderingFilter]

    def get_permissions(self):
        if self.action in ['list']:
            return [AllowAny()]
        elif self.action in ['like','create']:
            return [IsAuthenticated()]
        return []

    def get_queryset(self):
        community_id = self.kwargs.get("community_id")
        community = get_object_or_404(Community, id=community_id)
        return CommunityComment.objects.filter(community=community)

    def create(self, request, *args, **kwargs):
        community_id = self.kwargs.get("community_id")
        community = get_object_or_404(Community, id=community_id)
        
        comment = CommunityComment.objects.create(
            community=community,
            content=request.data['content'],
            writer=request.user
        )

        serializer = CommunityCommentSerializer(comment)
        return Response(serializer.data)

# 커뮤니티 댓글
class CommentViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = CommunityComment.objects.all()
    serializer_class=CommunityCommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_permissions(self):
        if self.action in ['retrieve','update','partial_update','destroy']:
            return [IsOwnerOrReadOnly()]
        return[]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        
        if 'content' in data:
            instance.content = data.get('content', instance.content)
            instance.updated_at = timezone.now()
            instance.save()
            
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "댓글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
    

# 전체 게시물
class CommunityListViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content', 'writer', 'cinema__name']
    pagination_class = CommunityPagination

    def get_permissions(self):
        return [AllowAny()]

    def get_queryset(self):
        return Community.objects.annotate(
            likes_cnt=Count('likes_community', distinct=True)
        )