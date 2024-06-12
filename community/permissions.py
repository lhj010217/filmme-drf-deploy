from rest_framework.permissions import BasePermission, SAFE_METHODS

# 권한 설정하는 파일
class IsOwnerOrReadOnly(BasePermission): # 작성자 아니면 읽기만 허용
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.writer == request.user or request.user.is_superuser