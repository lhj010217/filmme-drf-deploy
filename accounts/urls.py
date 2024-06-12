from django.urls import path, include
# from .oauth import *
from .views import *
from rest_framework import routers

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("signup", SignUpViewSet, basename="signup")

# user_profile_router = routers.SimpleRouter()
# user_profile_router.register("mypage/profile", UserViewSet, basename="mypage-profile")
app_name = "user"

urlpatterns = [
    path('accounts/', include(default_router.urls)),
    path('accounts/login', LoginAPIView.as_view(), name='login'),
    path('accounts/password/change', CustomPasswordChangeView.as_view(), name='rest_password_change'),
    path('accounts/password-reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password-reset', PasswordResetRequestView.as_view(), name='password_reset'),
    # 토큰
    path('accounts/token', TokenObtainPairView.as_view(), name='token_obtain_pair'), # refresh token, access token 확인
    path('accounts/token/refresh', TokenRefreshView.as_view(), name='token_refresh'), # refresh token 입력 시 새로운 access token
    #path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # 작성자 본인 확인
    path('users/check', CheckWriterAPIView.as_view(), name='check-writer'),
]