from rest_framework import serializers
from .models import Community, CommunityComment, CommunityImage, CommunityLike

from django.contrib.auth import get_user_model
from main.models import Cinema

from accounts.models import User

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'

class LikePostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityLike
        fields = '__all__'


# 이미지
class CommunityImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = CommunityImage
        fields = ['image']

# 댓글
class CommunityCommentSerializer(serializers.ModelSerializer):
    community = serializers.SerializerMethodField()
    writer = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()    

    def get_created_at(self, instance):
        return instance.created_at.strftime("%Y/%m/%d %H:%M")

    def get_updated_at(self, instance):
        return instance.updated_at.strftime("%Y/%m/%d %H:%M")
    
    def get_community(self, instance):
        return instance.community.id
    
    def get_writer(self, instance):
        return instance.writer.nickname
    
    class Meta:
        model = CommunityComment
        fields = '__all__'

# 커뮤니티 리스트 - tips
class TipListSerializer(serializers.ModelSerializer):
    # writer = serializers.CharField(source='writer.nickname', read_only=True)
    # is_liked = serializers.SerializerMethodField(read_only=True)
    likes_cnt = serializers.IntegerField(read_only=True)
    comments_cnt = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True) 
    cinema = serializers.SerializerMethodField(read_only=True)
    # ratings_cnt = serializers.IntegerField(read_only=True)
    rating = serializers.FloatField(read_only=True)

    def get_cinema(self, instance):
        cinema_instance = instance.cinema
        if cinema_instance is not None:
            return cinema_instance.name
        else:
            return None
        
    def get_created_at(self, instance):
        return instance.created_at.strftime("%Y/%m/%d %H:%M")

    def get_comments_cnt(self, instance):
        return instance.comments_community.count()
    
    class Meta:
        model = Community
        fields = [
            "id",
            "cinema",
            "category",
            "title",
            "comments_cnt",
            "view_cnt",
            "likes_cnt",
            "created_at",
            # "ratings_cnt",
            "rating"
        ]

# 커뮤니티 리스트 - commons
class CommonListSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField(read_only=True)
    likes_cnt = serializers.IntegerField(read_only=True)
    comments_cnt = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)

    # def get_cinema(self, instance):
    #     cinema_instance = instance.cinema
    #     if cinema_instance is not None:
    #         return cinema_instance.name
    #     else:
    #         return None
    
    def get_created_at(self, instance):
        return instance.created_at.strftime("%Y/%m/%d %H:%M")

    def get_comments_cnt(self, instance):
        return instance.comments_community.count()
    
    def get_is_liked(self, instance):

        # user = get_user(self.context['request'])
        User = get_user_model()
        user = self.context['request'].user if isinstance(self.context['request'].user, User) else None
        
        if user is not None:
            return CommunityLike.objects.filter(community=instance,user=user).exists()
        else:
            return False
    class Meta:
        model = Community
        fields = [
            "id",
            # "cinema",
            "category",
            "title",
            "comments_cnt",
            "view_cnt",
            "is_liked",
            "likes_cnt",
            "created_at"
        ]

# 커뮤니티 리스트 - suggestions
class SuggestionListSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField(read_only=True)
    likes_cnt = serializers.IntegerField(read_only=True)
    comments_cnt = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)
    cinema = serializers.SerializerMethodField(read_only=True)
    is_received = serializers.SerializerMethodField()
    can_edit_received = serializers.SerializerMethodField()

    def get_cinema(self, instance):
        cinema_instance = instance.cinema
        if cinema_instance is not None:
            if cinema_instance.name:
                return cinema_instance.name
            else:
                return "기타"
        else:
            return "기타"

    def get_created_at(self, instance):
        return instance.created_at.strftime("%Y/%m/%d %H:%M")

    def get_comments_cnt(self, instance):
        return instance.comments_community.count()

    def get_is_liked(self, instance):
        User = get_user_model()
        user = self.context['request'].user if isinstance(self.context['request'].user, User) else None
        if user is not None:
            return CommunityLike.objects.filter(community=instance, user=user).exists()
        else:
            return False

    def get_is_received(self, instance):
        return 'o' if instance.is_received else 'x'

    def get_can_edit_received(self, instance):
        user = self.context['request'].user
        return user.is_staff

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if 'is_received' in validated_data and user.is_staff:
            instance.is_received = validated_data['is_received']
            instance.save()
        return super().update(instance, validated_data)

    class Meta:
        model = Community
        fields = [
            "id",
            "cinema",
            "category",
            "title",
            "comments_cnt",
            "view_cnt",
            "is_liked",
            "likes_cnt",
            "created_at",
            "is_received",
            "can_edit_received",
        ]
        read_only_fields = ["is_received", "can_edit_received"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = self.context['request'].user
        if user.is_staff:
            representation['is_received'] = 'o' if instance.is_received else 'x'
        return representation


# 커뮤니티 디테일 - 자유게시판
class CommonDetailSerializer(serializers.ModelSerializer):
    writer = serializers.CharField(source='writer.nickname', read_only=True)
    images = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField(read_only=True)
    likes_cnt = serializers.IntegerField(read_only=True)
    comments_cnt = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()    

    def get_created_at(self, instance):
        return instance.created_at.strftime("%Y/%m/%d %H:%M")

    def get_updated_at(self, instance):
        return instance.updated_at.strftime("%Y/%m/%d %H:%M")

    def get_comments_cnt(self, instance):
        return instance.comments_community.count()
    
    def get_is_liked(self, instance):
        
        # user = get_user(self.context['request'])
        User = get_user_model()
        user = self.context['request'].user if isinstance(self.context['request'].user, User) else None
        if user is not None:
            return CommunityLike.objects.filter(community=instance,user=user).exists()
        else:
            return False
    
    # 등록된 이미지들 가져오기
    def get_images(self, obj):
        image = obj.images_community.all()
        return CommunityImageSerializer(instance=image, many=True, context=self.context).data

    class Meta:
        model = Community
        fields = [
            'id', 
            'category',
            'writer', 
            'title', 
            'content', 
            'is_liked', 
            'view_cnt',
            'comments_cnt',
            'likes_cnt', 
            'images', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = [
            'id', 
            'created_at', 
            'updated_at'
        ]

# 커뮤니티 디테일 - cinema_tip
class Cinema_tipDetailSerializer(serializers.ModelSerializer):
    cinema = serializers.CharField(source='cinema.name', read_only=True)
    writer = serializers.CharField(source='writer.nickname', read_only=True)
    images = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField(read_only=True)
    likes_cnt = serializers.IntegerField(read_only=True)
    comments_cnt = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    # ratings_cnt = serializers.IntegerField(read_only=True)    
    rating = serializers.FloatField(read_only=True)

    def get_created_at(self, instance):
        return instance.created_at.strftime("%Y/%m/%d %H:%M")

    def get_updated_at(self, instance):
        return instance.updated_at.strftime("%Y/%m/%d %H:%M")

    def get_comments_cnt(self, instance):
        return instance.comments_community.count()
    
    def get_is_liked(self, instance):
        # user = get_user(self.context['request'])
        User = get_user_model()
        user = self.context['request'].user if isinstance(self.context['request'].user, User) else None
        if user is not None:
            return CommunityLike.objects.filter(community=instance,user=user).exists()
        else:
            return False
    # 등록된 이미지들 가져오기
    def get_images(self, obj):
        image = obj.images_community.all()
        return CommunityImageSerializer(instance=image, many=True, context=self.context).data

    class Meta:
        model = Community
        fields = [
            'id', 
            'category',
            'cinema',
            'writer', 
            'title', 
            'content', 
            'is_liked', 
            'view_cnt',
            'comments_cnt',
            'likes_cnt', 
            'images', 
            'created_at', 
            'updated_at',
            # 'ratings_cnt',
            'rating'
        ]
        read_only_fields = [
            'id', 
            'created_at', 
            'updated_at'
        ]

# 커뮤니티 디테일 - suggestion
class SuggestionDetailSerializer(serializers.ModelSerializer):
    cinema = serializers.CharField(source='cinema.name', read_only=True)
    writer = serializers.CharField(source='writer.nickname', read_only=True)
    images = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField(read_only=True)
    likes_cnt = serializers.IntegerField(read_only=True)
    comments_cnt = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, instance):
        return instance.created_at.strftime("%Y/%m/%d %H:%M")

    def get_updated_at(self, instance):
        return instance.updated_at.strftime("%Y/%m/%d %H:%M")

    def get_comments_cnt(self, instance):
        return instance.comments_community.count()
    
    def get_is_liked(self, instance):
        # user = get_user(self.context['request'])
        User = get_user_model()
        user = self.context['request'].user if isinstance(self.context['request'].user, User) else None
        if user is not None:
            return CommunityLike.objects.filter(community=instance,user=user).exists()
        else:
            return False
        
    # 등록된 이미지들 가져오기
    def get_images(self, obj):
        image = obj.images_community.all()
        return CommunityImageSerializer(instance=image, many=True, context=self.context).data

    class Meta:
        model = Community
        fields = [
            'id', 
            'category',
            'writer', 
            'title', 
            'content', 
            'cinema',
            'is_liked', 
            'view_cnt',
            'comments_cnt',
            'likes_cnt', 
            'images', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = [
            'id', 
            'created_at', 
            'updated_at'
        ]
    
# 게시물 작성 & 수정
class CommunityCreateUpdateSerializer(serializers.ModelSerializer):
    writer = serializers.CharField(source='writer.nickname', read_only=True)
    images = serializers.ListField(child=serializers.ImageField(), required=False)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    cinema = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    rating = serializers.FloatField(required=False)

    def clear_existing_images(self, instance):
        for community_image in instance.images_community.all():
            community_image.image.delete()
            community_image.delete()

    def get_created_at(self, instance):
        return instance.created_at.strftime("%Y/%m/%d %H:%M")

    def get_updated_at(self, instance):
        return instance.updated_at.strftime("%Y/%m/%d %H:%M")
    
    # 게시물 작성 함수
    def create(self, validated_data):
        category = validated_data.get('category')
        cinema_title = validated_data.get('cinema')
        rating = validated_data.get('rating')

        if category == 'cinema_tip' and (cinema_title is None or cinema_title == ""):
            raise serializers.ValidationError("영화관 후기 게시물을 작성할 때는 영화관을 선택(입력)해주세요.")
        if category == 'cinema_tip' and (rating is None or rating not in [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]):
            raise serializers.ValidationError("평점은 1점에서 5점 사이로 입력해주세요.")
        
        cinema_instance = None
        if cinema_title:
            try:
                cinema_instance = Cinema.objects.get(name=cinema_title)
            except Cinema.DoesNotExist:
                raise serializers.ValidationError("존재하지 않는 영화관입니다.")
        
        image_data = self.context['request'].FILES
        user = self.context['request'].user
        validated_data['writer'] = user
        validated_data['cinema'] = cinema_instance 
        instance = Community.objects.create(**validated_data)

        for image_data in image_data.getlist('image'):
            CommunityImage.objects.create(community=instance, image=image_data)
        return instance
    
    # def validate(self, attrs):
    #     category = attrs.get('category')
    #     rating = attrs.get('rating')
    #     user = self.context['request'].user

    #     if category == 'cinema_tip' and rating is not None:
    #         if attrs.get('writer') != user:
    #             raise serializers.ValidationError("글 작성자만 평점을 등록할 수 있습니다.")

    #     return attrs
    
    # 게시물 수정 함수
    def update(self, instance, validated_data):
        cinema_title = validated_data.get('cinema')
        rating = validated_data.get('rating')

        if 'category' in validated_data and validated_data['category'] == 'cinema_tip':
            if rating is None or rating not in [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]:
                raise serializers.ValidationError("평점은 1점에서 5점 사이로 입력해주세요.")
            
        cinema_instance = None
        if cinema_title:
            try:
                cinema_instance = Cinema.objects.get(name=cinema_title)
            except Cinema.DoesNotExist:
                raise serializers.ValidationError("존재하지 않는 영화관입니다.")
        
        image_data = self.context['request'].FILES
        validated_data['cinema'] = cinema_instance 
        self.clear_existing_images(instance)
        for image_data in image_data.getlist('image'):
            CommunityImage.objects.create(community=instance, image=image_data)
        return super().update(instance, validated_data)
    
    #이미지 삭제    
    def clear_existing_images(self, instance):
            instance.images.all().delete()    

    class Meta:
        model = Community
        fields = ['id', 'cinema', 'writer', 'category', 'title', 'content', 'images', 'created_at', 'updated_at', 'rating']
        read_only_fields = ['id', 'created_at', 'updated_at']